#!/bin/bash
# Script de arranque en PRODUCCIÓN para Linux (Gunicorn)
# Uso: chmod +x start_production.sh && ./start_production.sh

set -e

# Ir al directorio del script
cd "$(dirname "$0")"

echo "========================================"
echo "  Iniciando Analista de Licitaciones (PRODUCCION)"
echo "========================================"

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "ADVERTENCIA: No se encontro .env. Copia .env.example a .env y configuralo."
    echo ""
fi

# Activar entorno virtual si existe
if [ -d .venv ]; then
    source .venv/bin/activate
else
    echo "ERROR: No se encontro el entorno virtual .venv. Ejecuta 'uv sync' primero."
    exit 1
fi

# Mostrar configuracion
echo "Puerto: ${FLASK_PORT:-5000}"
echo "Host: ${FLASK_HOST:-0.0.0.0}"
echo "Debug: ${FLASK_DEBUG:-0}"
echo ""

# Iniciar con Gunicorn (servidor WSGI de producción para Linux)
echo "Iniciando servidor Gunicorn en http://${FLASK_HOST:-0.0.0.0}:${FLASK_PORT:-5000}..."
gunicorn --bind ${FLASK_HOST:-0.0.0.0}:${FLASK_PORT:-5000} --workers 4 --timeout 120 'wsgi:create_app()'