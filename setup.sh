#!/bin/bash
# setup.sh — Configura el entorno local (Docker Compose, .env, SSL, Nginx y seeds de Django).
# Uso: ./setup.sh [dev|prod] [--no-seed]  — detalle en ./setup.sh --help
set -Eeuo pipefail

# ── Constantes ────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly ROOT_DIR="${SCRIPT_DIR}"

readonly ENV_FILE="${ROOT_DIR}/src/.env"
readonly ENV_EXAMPLE="${ROOT_DIR}/src/.env.example"
readonly COMPOSE_FILE="${ROOT_DIR}/config/docker-compose.yml"

readonly DEFAULT_DOMAIN="medicare.service.test"
readonly NGINX_DIR="${ROOT_DIR}/config/nginx"
readonly NGINX_TEMPLATE="${NGINX_DIR}/default.conf.template"
readonly NGINX_CONF="${NGINX_DIR}/default.conf"
readonly NGINX_CERTS="${NGINX_DIR}/certs"

readonly DEFAULT_MODE="dev"
readonly DB_SERVICE="db"
readonly DJANGO_SERVICE="django_backend"
readonly DJANGO_WORKDIR="/workspace/src"
readonly SEED_CMD=(python manage.py seed_all)

readonly WAIT_TIMEOUT=120
readonly WAIT_INTERVAL=3

LOCAL_UID="$(id -u)"
readonly LOCAL_UID
LOCAL_GID="$(id -g)"
readonly LOCAL_GID
readonly DEVCONTAINER_USER="vscode"
export LOCAL_UID LOCAL_GID DEVCONTAINER_USER

# Mutable por parse_args
MODE_ARG=""
SEED_ENABLED=true

# ── Colores (desactivados sin TTY o con NO_COLOR) ─────────────────────────────
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
    readonly C_CYAN="\033[1;36m"
    readonly C_GREEN="\033[1;32m"
    readonly C_YELLOW="\033[1;33m"
    readonly C_RED="\033[1;31m"
    readonly C_RESET="\033[0m"
else
    readonly C_CYAN=""
    readonly C_GREEN=""
    readonly C_YELLOW=""
    readonly C_RED=""
    readonly C_RESET=""
fi

# ── Logging ───────────────────────────────────────────────────────────────────
_log() {
    local color="$1"
    local tag="$2"
    shift 2
    printf '%b%s%b %b%b\n' "${color}" "${tag}" "${C_RESET}" "$*" "${C_RESET}"
}

info()    { _log "${C_CYAN}"   "[INFO] " "$@"; }
success() { _log "${C_GREEN}"  "[OK]    " "$@"; }
warn()    { _log "${C_YELLOW}" "[WARN]  " "$@"; }
error()   { _log "${C_RED}"    "[ERROR] " "$@" >&2; }
fatal()   { error "$@"; exit 1; }

# ── Manejo de errores ─────────────────────────────────────────────────────────
handle_error() {
    local status=$?
    error "Fallo en ${0##*/}:${BASH_LINENO[0]} — comando: ${BASH_COMMAND} (exit ${status})"
    exit "${status}"
}
trap handle_error ERR

# ── Utilidades ────────────────────────────────────────────────────────────────
require_cmd() {
    local cmd="$1"
    if ! command -v "${cmd}" >/dev/null 2>&1; then
        fatal "Comando requerido no encontrado: ${cmd}"
    fi
}

ensure_directory() {
    local dir="$1"
    [ -d "${dir}" ] && return 0
    if ! mkdir -p "${dir}"; then
        fatal "No se pudo crear el directorio: ${dir}"
    fi
}

# Crea el archivo solo si no existe; recibe el contenido por stdin.
ensure_file() {
    local file="$1"
    local rel="${file#"${ROOT_DIR}"/}"
    if [ -f "${file}" ]; then
        info "${rel} ya existe, no se modifica"
        return 0
    fi
    if ! cat >"${file}"; then
        fatal "No se pudo escribir: ${rel}"
    fi
    success "Creado ${rel}"
}

normalize_mode() {
    local mode="${1:-${DEFAULT_MODE}}"
    printf '%s' "${mode}" | tr '[:upper:]' '[:lower:]'
}

# Lee una clave KEY=VALUE de un archivo .env; vacío si no existe. Último valor gana.
env_get() {
    local key="$1"
    local file="$2"
    sed -n "s/^${key}=//p" "${file}" 2>/dev/null | tail -n1
}

# DOMAIN se lee del .env; si no está definido, usa el valor por defecto.
# El warn va a stderr para no contaminar el valor devuelto por stdout.
resolve_domain() {
    local domain=""
    domain="$(env_get "DOMAIN" "${ENV_FILE}" || true)"
    if [ -z "${domain}" ]; then
        warn "DOMAIN no está definido en ${ENV_FILE}; usando '${DEFAULT_DOMAIN}'" >&2
        domain="${DEFAULT_DOMAIN}"
    fi
    printf '%s' "${domain}"
}

is_prod() {
    [[ "${APP_MODE}" == "prod" ]]
}

build_target_for_mode() {
    if is_prod; then
        printf 'production'
    else
        printf 'development'
    fi
}

# Único punto de acceso a Docker Compose (DRY).
compose() {
    local args=(-f "${COMPOSE_FILE}")
    if is_prod; then
        args+=(--profile prod)
    fi
    docker compose "${args[@]}" "$@"
}

check_dependencies() {
    require_cmd docker
    if ! docker compose version >/dev/null 2>&1; then
        fatal "Docker Compose v2 no está disponible. Instala el plugin 'docker compose'."
    fi
    if is_prod; then
        require_cmd openssl
    fi
}

# ── Paso 1: variables de entorno ──────────────────────────────────────────────
setup_env_files() {
    ensure_file "${ENV_EXAMPLE}" <<'EOF'
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_PORT=5432
APP_PORT=8000
DJANGO_SETTINGS_MODULE=myapp.settings
DJANGO_DIR=/workspace/src
DOMAIN=medicare.service.test
EOF

    if [ -f "${ENV_FILE}" ]; then
        info "src/.env ya existe, no se modifica"
        return 0
    fi
    if ! cp "${ENV_EXAMPLE}" "${ENV_FILE}"; then
        fatal "No se pudo copiar el ejemplo a src/.env"
    fi
    success "Creado src/.env desde el ejemplo"
}

# ── Paso 2 (solo prod): certificados SSL, Nginx y /etc/hosts ─────────────────
setup_ssl_cert() {
    ensure_directory "${NGINX_CERTS}"

    # Si falta solo uno de los dos, se regeneran ambos (van siempre juntos).
    if [ -f "${CERT}" ] && [ -f "${KEY}" ]; then
        info "Certificado SSL ya existe, no se regenera"
        return 0
    fi

    info "Generando certificado SSL autofirmado para ${DOMAIN}..."
    if ! openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
        -keyout "${KEY}" -out "${CERT}" \
        -subj "/CN=${DOMAIN}" \
        -addext "subjectAltName=DNS:${DOMAIN},DNS:localhost,IP:127.0.0.1"; then
        fatal "No se pudo generar el certificado SSL"
    fi
    success "Certificado creado en ${NGINX_CERTS}/"
}

setup_nginx_conf() {
    ensure_directory "${NGINX_DIR}"

    if [ -f "${NGINX_CONF}" ]; then
        info "config/nginx/default.conf ya existe, no se modifica"
        return 0
    fi
    if [ ! -f "${NGINX_TEMPLATE}" ]; then
        fatal "Plantilla de Nginx no encontrada: ${NGINX_TEMPLATE}"
    fi

    # La plantilla es versionada; aquí solo se renderiza con la constante DOMAIN.
    if ! sed "s/__DOMAIN__/${DOMAIN}/g" "${NGINX_TEMPLATE}" >"${NGINX_CONF}"; then
        fatal "No se pudo renderizar la plantilla de Nginx"
    fi
    success "Creado config/nginx/default.conf"
}

ensure_hosts_entry() {
    local entry="127.0.0.1 ${DOMAIN}"
    if grep -qE "^127\.0\.0\.1[[:space:]]+${DOMAIN}([[:space:]]|\$)" /etc/hosts; then
        info "${DOMAIN} ya está en /etc/hosts"
        return 0
    fi

    info "Agregando '${entry}' a /etc/hosts (puede pedir sudo)..."
    if [ "$(id -u)" -eq 0 ]; then
        printf '%s\n' "${entry}" >>/etc/hosts
    else
        require_cmd sudo
        if ! printf '%s\n' "${entry}" | sudo tee -a /etc/hosts >/dev/null; then
            fatal "No se pudo modificar /etc/hosts. Ejecútalo manualmente: echo '${entry}' | sudo tee -a /etc/hosts"
        fi
    fi
    success "Agregado '${entry}' a /etc/hosts"
}

# ── Paso 3: levantar servicios y esperar readiness real ──────────────────────
# Espera healthcheck del contenedor; si no tiene healthcheck, basta "running".
wait_for_service() {
    local service="$1"
    local container_id=""
    local status=""
    local health=""
    local deadline=$((SECONDS + WAIT_TIMEOUT))

    info "Esperando a que '${service}' esté listo..."
    while [ "${SECONDS}" -lt "${deadline}" ]; do
        container_id="$(compose ps -q "${service}" 2>/dev/null || true)"
        status="$(docker inspect --format '{{.State.Status}}' "${container_id}" 2>/dev/null || true)"
        health="$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "${container_id}" 2>/dev/null || true)"
        if [[ "${status}" == "running" && ("${health}" == "none" || "${health}" == "healthy") ]]; then
            success "'${service}' listo"
            return 0
        fi
        sleep "${WAIT_INTERVAL}"
    done

    fatal "Timeout esperando a '${service}' (${WAIT_TIMEOUT}s).\nLogs:\n$(docker logs --tail 20 "${container_id}" 2>&1 || true)"
}

# Espera la señal de arranque real de la app en los logs (aparece después de
# las migraciones del entrypoint, garantizando que el seed es seguro).
wait_for_app_ready() {
    local service="$1"
    local container_id=""
    local deadline=$((SECONDS + WAIT_TIMEOUT))

    info "Esperando a que '${service}' complete su arranque..."
    while [ "${SECONDS}" -lt "${deadline}" ]; do
        container_id="$(compose ps -q "${service}" 2>/dev/null || true)"
        if [ -n "${container_id}" ] && docker logs --tail 500 "${container_id}" 2>&1 | grep -qE "Starting development server|Starting gunicorn"; then
            success "'${service}' arrancó correctamente"
            return 0
        fi
        sleep "${WAIT_INTERVAL}"
    done

    fatal "Timeout: '${service}' no arrancó en ${WAIT_TIMEOUT}s.\nÚltimos logs:\n$(docker logs --tail 40 "${container_id}" 2>&1 || true)"
}

up_services() {
    info "Construyendo imágenes y levantando servicios..."
    compose up --build -d
    wait_for_service "${DB_SERVICE}"
    wait_for_service "${DJANGO_SERVICE}"
    wait_for_app_ready "${DJANGO_SERVICE}"
    success "Servicios listos"
}

# ── Paso 4: seed de datos ─────────────────────────────────────────────────────
run_seed() {
    if [ "${SEED_ENABLED}" != "true" ]; then
        warn "Seed omitido (--no-seed)"
        return 0
    fi

    info "Ejecutando seed..."
    if ! compose exec -T -w "${DJANGO_WORKDIR}" "${DJANGO_SERVICE}" "${SEED_CMD[@]}"; then
        fatal "El seed falló. Revisa los logs con: docker compose -f config/docker-compose.yml logs ${DJANGO_SERVICE}"
    fi
    success "Seed completado"
}

print_summary() {
    cat <<EOF

Entorno listo (modo: ${APP_MODE}).

Comandos útiles:
  export LOCAL_UID=${LOCAL_UID}
  export LOCAL_GID=${LOCAL_GID}
  docker compose -f config/docker-compose.yml up --build
  docker compose -f config/docker-compose.yml exec django_backend bash

VS Code Dev Containers:
  1. Abrir esta carpeta en VS Code
  2. Ejecutar "Dev Containers: Reopen in Container"
EOF
}

# ── Argumentos ────────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Uso: $(basename "$0") [dev|prod] [--no-seed]

Modo (por defecto: dev):
  dev      Entorno de desarrollo (runserver de Django)
  prod     Entorno de producción local (Gunicorn + Nginx + SSL + /etc/hosts)

Opciones:
  -h, --help  Muestra esta ayuda
  --no-seed   Omite la ejecución del seed de datos

Ejemplos:
  $0                  Entorno de desarrollo
  $0 prod             Entorno de producción local
  $0 dev --no-seed    Dev sin seed de datos
EOF
}

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            --no-seed)
                SEED_ENABLED=false
                ;;
            dev|prod)
                if [ -n "${MODE_ARG}" ]; then
                    fatal "Modo duplicado: '${1}' (ya se indicó '${MODE_ARG}')"
                fi
                MODE_ARG="$1"
                ;;
            *)
                fatal "Argumento desconocido: '${1}'. Ejecuta '$(basename "$0") --help'."
                ;;
        esac
        shift
    done
}

# ── Punto de entrada ──────────────────────────────────────────────────────────
main() {
    parse_args "$@"

    APP_MODE="$(normalize_mode "${MODE_ARG:-${DEFAULT_MODE}}")"
    readonly APP_MODE
    export APP_MODE
    BUILD_TARGET="$(build_target_for_mode)"
    readonly BUILD_TARGET
    export BUILD_TARGET

    check_dependencies

    info "Setting Up (modo: ${APP_MODE})"

    setup_env_files
    if is_prod; then
        DOMAIN="$(resolve_domain)"
        readonly DOMAIN
        CERT="${NGINX_CERTS}/${DOMAIN}.crt"
        readonly CERT
        KEY="${NGINX_CERTS}/${DOMAIN}.key"
        readonly KEY
        setup_ssl_cert
        setup_nginx_conf
        ensure_hosts_entry
    fi

    up_services
    run_seed
    print_summary
    success "Setup completado"
}

main "$@"
