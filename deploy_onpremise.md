# Guía de Despliegue On-Premise - Analista de Licitaciones Públicas
# MVP para Contratación Administrativa de Costa Rica (SICOP, BCCR)

Este documento describe cómo desplegar la aplicación en un servidor local (on-premise),
tanto en Windows como en Linux.

---

## 1. ARQUITECTURA DE DESPLIEGUE

```
[Usuario] <-> [Navegador Web] <-> [Servidor WSGI de Producción] <-> [App Flask]
                                            |
                                    (Waitress en Windows / Gunicorn en Linux)
```

La aplicación no requiere base de datos. Todo se procesa en memoria a partir de los
archivos de insumos subidos por el usuario.

---

## 2. REQUISITOS DEL SERVIDOR

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Sistema operativo | Windows 10 / Server 2019 | Windows Server 2022 / Linux (Ubuntu 22.04+) |
| Python | 3.9+ | 3.11+ |
| RAM | 2 GB | 4 GB+ |
| Espacio en disco | 1 GB | 5 GB+ |
| Red | Puerto 5000 libre | Puerto 80/443 con reverso proxy |

---

## 3. PREPARACIÓN DEL ENTORNO

### 3.1 Instalar Python y uv

**Windows:**
```powershell
# Instalar uv
irm https://astral.sh/uv/install.ps1 | iex
# Instalar Python 3.11
uv python install 3.11
```

**Linux (Ubuntu/Debian):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.11
```

### 3.2 Clonar o copiar el proyecto

Copiar la carpeta del proyecto al servidor destino:
```
C:\inetpub\wwwroot\analista-licitaciones\   (Windows)
/var/www/analista-licitaciones/             (Linux)
```

### 3.3 Crear entorno virtual e instalar dependencias

```bash
uv sync
```

Esto instalará: `flask`, `python-dotenv`, `python-docx`, `pytest` (dev),
y `waitress` (Windows) o `gunicorn` (Linux).

---

## 4. CONFIGURACIÓN DE VARIABLES DE ENTORNO

### 4.1 Copiar .env.example a .env

```bash
copy .env.example .env          (Windows)
cp .env.example .env            (Linux)
```

### 4.2 Editar .env con valores de producción

```ini
# OBLIGATORIO: Generar una llave secreta segura
# Windows PowerShell: [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes(32) | ForEach-Object { "{0:x2}" -f $_ } -join ''
# Linux: python -c "import secrets; print(secrets.token_hex(32))"
FLASK_SECRET_KEY=tu-llave-secreta-aqui-de-64-caracteres

# Llave del agente de IA (opcional; modo fallback si está vacía)
AGENTE_IA_KEY=tu-llave-de-api-del-agente-ia

# Puerto y host
FLASK_PORT=5000
FLASK_HOST=0.0.0.0

# Debug DESACTIVADO en producción
FLASK_DEBUG=0
```

### 4.3 Proteger el archivo .env

**Windows:**
```powershell
icacls .env /inheritance:r
icacls .env /grant:r "Usuarios:R"
icacls .env /grant "SISTEMA:F"
icacls .env /grant "Administradores:F"
```

**Linux:**
```bash
chmod 600 .env
chown root:www-data .env
```

---

## 5. DESPLIEGUE EN WINDOWS (Waitress)

Waitress es un servidor WSGI puro en Python, ideal para Windows sin necesidad de compiladores C++.

### 5.1 Instalar waitress

```bash
uv add waitress
```

### 5.2 Ejecutar en producción

```bat
start_production.bat
```

O directamente:
```bat
waitress-serve --call 'wsgi:create_app' --host 0.0.0.0 --port 5000
```

### 5.3 Instalar como servicio de Windows (opcional)

Usar NSSM (Non-Sucking Service Manager):
```bat
nssm install AnalistaLicitaciones "C:\ruta\al\proyecto\.venv\Scripts\python.exe"
nssm set AnalistaLicitaciones AppParameters "-m waitress --call wsgi:create_app --host 0.0.0.0 --port 5000"
nssm set AnalistaLicitaciones AppDirectory "C:\ruta\al\proyecto"
nssm start AnalistaLicitaciones
```

---

## 6. DESPLIEGUE EN LINUX (Gunicorn + systemd)

### 6.1 Instalar gunicorn

```bash
uv add gunicorn
```

### 6.2 Crear servicio systemd

`/etc/systemd/system/analista-licitaciones.service`:
```ini
[Unit]
Description=Analista de Licitaciones Públicas
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/analista-licitaciones
EnvironmentFile=/var/www/analista-licitaciones/.env
ExecStart=/var/www/analista-licitaciones/.venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 'wsgi:create_app()'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 6.3 Activar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable analista-licitaciones
sudo systemctl start analista-licitaciones
sudo systemctl status analista-licitaciones
```

---

## 7. REVERSO PROXY (OPCIONAL PERO RECOMENDADO)

Para acceder por puerto 80/443 con HTTPS, usar Nginx como reverso proxy.

### 7.1 Nginx en Linux

`/etc/nginx/sites-available/analista-licitaciones`:
```nginx
server {
    listen 80;
    server_name tu-servidor.local;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/analista-licitaciones/app/static/;
    }
}
```

### 7.2 HTTPS con Certbot

```bash
sudo certbot --nginx -d tu-servidor.local
```

---

## 8. ARCHIVOS CREADO PARA DESPLIEGUE

| Archivo | Propósito |
|---------|-----------|
| `start_production.bat` | Arranque en producción para Windows (Waitress) |
| `start_production.sh` | Arranque en producción para Linux (Gunicorn) |
| `.env.example` | Plantilla de variables de entorno (subir a Git) |
| `.env` | Variables reales (NO subir a Git) |
| `pyproject.toml` | Dependencias del proyecto |
| `.gitignore` | Archivos que no se suben a Git (.env, .venv, etc.) |

---

## 9. VERIFICACIÓN DEL DESPLIEGUE

1. Abrir el navegador en `http://localhost:5000` (o la IP del servidor)
2. Verificar que carga la pantalla de inicio
3. Subir un archivo .docx de prueba
4. Verificar que `/resultados` muestra el JSON extraído
5. Verificar que `/descargar` descarga el JSON correctamente
6. Revisar los logs del servidor para errores

---

## 10. SEGURIDAD EN PRODUCCIÓN

| Medida | Estado | Acción |
|--------|--------|--------|
| SECRET_KEY desde .env | ✅ Implementado | Generar llave única por despliegue |
| Debug desactivado | ✅ Implementado | FLASK_DEBUG=0 en .env |
| Límite de subida (16 MB) | ✅ Implementado | MAX_CONTENT_LENGTH en app |
| .env no subido a Git | ✅ Implementado | En .gitignore |
| HTTPS | ⚠️ Pendiente | Configurar reverso proxy + Certbot |
| Reverso proxy | ⚠️ Pendiente | Nginx/IIS frente a Waitress/Gunicorn |
| Autenticación | ⚠️ Pendiente | Agregar si se requiere acceso restringido |

---

## 11. SOLUCIÓN DE PROBLEMAS

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Puerto 5000 ya en uso | Otro servicio usando el puerto | Cambiar FLASK_PORT en .env |
| Error de importación | Entorno virtual no activado | Ejecutar `uv sync` y activar .venv |
| SECRET_KEY hardcodeado | .env no cargado | Verificar que .env existe y se lee |
| Archivo .docx no se lee | python-docx no instalado | Ejecutar `uv sync` |
| PDF escaneado sin texto | Limitación del formato | El PDF necesita OCR previo |

---

## 12. RESUMEN RÁPIDO (Windows)

```powershell
# 1. Instalar uv y Python
irm https://astral.sh/uv/install.ps1 | iex
uv python install 3.11

# 2. Entrar al proyecto y sincronizar
cd C:\ruta\al\proyecto
uv sync

# 3. Configurar .env
copy .env.example .env
# Editar .env con FLASK_SECRET_KEY y AGENTE_IA_KEY

# 4. Iniciar en producción
start_production.bat

# 5. Abrir navegador
start http://localhost:5000
```

---

*Documento generado para despliegue on-premise del Analista de Licitaciones Públicas (MVP).*