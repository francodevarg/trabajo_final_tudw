#!/bin/bash
set -euo pipefail

MODE="${APP_MODE:-${1:-dev}}"
DJANGO_DIR="${DJANGO_DIR:-/workspace/src}"
MANAGE_PY="${DJANGO_DIR}/manage.py"

echo "------------------------------------------"
echo " Entrypoint | modo: ${MODE}"
echo " Proyecto   | ${DJANGO_DIR}"
echo "------------------------------------------"

if [ -f "/workspace/.venv/bin/activate" ]; then
    source /workspace/.venv/bin/activate
fi

wait_for_db() {
    echo "⏳ Esperando base de datos..."
    until python - <<'PY' 2>/dev/null
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "myapp.settings"))
django.setup()
from django.db import connection
connection.ensure_connection()
PY
    do
        sleep 2
    done
    echo "✅ Base de datos lista"
}

run_django() {
    cd "$DJANGO_DIR"
    wait_for_db

    echo "⚙️ Aplicando migraciones..."
    python manage.py migrate --noinput

    python manage.py collectstatic --noinput --clear >/dev/null 2>&1 || true

    if [ "$MODE" = "prod" ]; then
        echo "🚀 Iniciando Gunicorn (PROD)..."
        exec gunicorn myapp.wsgi:application \
            --bind 0.0.0.0:8000 \
            --workers "${GUNICORN_WORKERS:-3}" \
            --timeout "${GUNICORN_TIMEOUT:-120}" \
            --access-logfile - \
            --error-logfile -
    fi

    echo "🧪 Iniciando servidor de desarrollo..."
    exec python manage.py runserver 0.0.0.0:8000
}

if [ ! -d "$DJANGO_DIR" ]; then
    echo "❌ La ruta ${DJANGO_DIR} no existe."
    exec sleep infinity
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo "❌ No se encontro ${MANAGE_PY}."
    exec sleep infinity
fi

run_django