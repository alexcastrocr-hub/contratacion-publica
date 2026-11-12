# Script de arranque en PRODUCCIÓN para Windows (Waitress)
@echo off
:: Script de arranque de producción de la aplicación Analista de Licitaciones
:: Usa Waitress como servidor WSGI de producción

setlocal

:: Ir al directorio del script
cd /d "%~dp0"

echo ========================================
echo  Iniciando Analista de Licitaciones (PRODUCCION)
echo ========================================

:: Verificar que existe .env
if not exist .env (
    echo ADVERTENCIA: No se encontro .env. Copia .env.example a .env y configuralo.
    echo.
    pause
)

:: Activar entorno de uv si existe
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: No se encontro el entorno virtual .venv. Ejecuta 'uv sync' primero.
    pause
    exit /b 1
)

:: Mostrar configuracion
echo Puerto: %FLASK_PORT%
echo Host: %FLASK_HOST%
echo Debug: %FLASK_DEBUG%
echo.

:: Iniciar con Waitress (servidor WSGI de producción para Windows)
echo Iniciando servidor Waitress en http://%FLASK_HOST%:%FLASK_PORT%...
waitress-serve --call 'wsgi:create_app' --host %FLASK_HOST% --port %FLASK_PORT%

endlocal