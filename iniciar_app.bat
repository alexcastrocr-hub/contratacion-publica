@echo off
:: Script de arranque de la aplicación Analista de Licitaciones
:: Activa el entorno de uv, ejecuta la app y abre el navegador

setlocal

:: Ir al directorio del script
cd /d "%~dp0"

echo Iniciando la aplicación Analista de Licitaciones...

:: Ejecutar la app con uv
uv run python wsgi.py

:: Abrir el navegador en la URL de la app
start http://localhost:5000/

endlocal