"""Paquete principal de la aplicación Flask."""
import os
from flask import Flask


def create_app():
    """Crea y configura la aplicación Flask (patrón Application Factory)."""
    app = Flask(__name__, instance_relative_config=True)

    # Cargar variables de entorno desde .env si existe
    from dotenv import load_dotenv
    load_dotenv()

    # Configuración básica - SECRET_KEY desde .env (obligatorio en producción)
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-key-cambiar-en-produccion")
    app.config["JSON_AS_ASCII"] = False  # permitir acentos en JSON
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB límite subida de archivos

    # Registrar blueprints
    from app.controllers import bp_main
    app.register_blueprint(bp_main)

    return app