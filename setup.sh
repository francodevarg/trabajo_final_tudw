#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ROOT_DIR}/src/.env"
ENV_EXAMPLE="${ROOT_DIR}/src/.env.example"

MODE="${1:-dev}"

export APP_MODE="$MODE"

if [ "$APP_MODE" = "prod" ]; then
  export BUILD_TARGET="production"
else
  export BUILD_TARGET="development"
fi

echo "🚀 Setting Up"
echo "Modo: $APP_MODE"

if [ ! -f "$ENV_EXAMPLE" ]; then
    cat <<'EOF' > "$ENV_EXAMPLE"
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_PORT=5432
APP_PORT=8000
DJANGO_SETTINGS_MODULE=myapp.settings
DJANGO_DIR=/workspace/src
EOF
    echo "Creado src/.env.example"
fi

if [ ! -f "$ENV_FILE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "Creado src/.env desde el ejemplo"
else
    echo "src/.env ya existe, no se modifica"
fi

export LOCAL_UID="$(id -u)"
export LOCAL_GID="$(id -g)"
export DEVCONTAINER_USER="vscode"

echo "Construyendo imagenes..."
docker compose -f "${ROOT_DIR}/config/docker-compose.yml" up --build -d

echo "Esperando a que el contenedor este listo..."
sleep 15

echo "Ejecutando seed..."
docker compose -f "${ROOT_DIR}/config/docker-compose.yml" \
  exec -w /workspace/src \
  django_backend python manage.py seed_all
cat <<EOF

Entorno listo.

Comandos utiles:
  export LOCAL_UID=${LOCAL_UID}
  export LOCAL_GID=${LOCAL_GID}
  docker compose -f config/docker-compose.yml up --build
  docker compose -f config/docker-compose.yml exec django_backend bash

VS Code Dev Containers:
  1. Abrir esta carpeta en VS Code
  2. Ejecutar "Dev Containers: Reopen in Container"
EOF
