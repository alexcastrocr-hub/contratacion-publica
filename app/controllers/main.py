"""Blueprint base con rutas principales."""
from flask import Blueprint, render_template, request, jsonify, send_file, session, redirect, url_for
import os
import io

from app.services.agente_ia import analizar_licitacion_json, analizar_licitacion

bp_main = Blueprint("main", __name__)


@bp_main.before_request
def requerir_autenticacion():
    """Regla de acceso: todas las rutas exigen sesión, excepto /login, /salir y estáticos."""
    rutas_libres = ["main.login", "main.salir", "static"]
    if request.endpoint and not any(request.endpoint.startswith(r) for r in rutas_libres):
        if "usuario" not in session:
            return redirect(url_for("main.login"))


@bp_main.route("/login", methods=["GET", "POST"])
def login():
    """Pantalla de inicio de sesión."""
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")
        usuario_valido = os.environ.get("APP_USUARIO", "")
        clave_valida = os.environ.get("APP_CLAVE", "")
        if usuario == usuario_valido and clave == clave_valida:
            session["usuario"] = usuario
            return redirect(url_for("main.inicio"))
        else:
            error = "Usuario o contraseña incorrectos"
    return render_template("login.html", error=error)


@bp_main.route("/salir")
def salir():
    """Cerrar sesión y redirigir al login."""
    session.pop("usuario", None)
    return redirect(url_for("main.login"))


@bp_main.route("/")
def inicio():
    """Pantalla de inicio de la aplicación."""
    return render_template("inicio.html")


@bp_main.route("/resultados")
def resultados():
    """Pantalla de resultados del análisis."""
    resultado_json = request.args.get("json")
    return render_template("resultados.html", json_previo=resultado_json)


@bp_main.route("/detalle/<campo>")
def detalle(campo):
    """
    Muestra el detalle de un campo específico del JSON de resultados.
    Recibe el nombre del campo (ej. 'identificacion_concurso.numero_licitacion')
    y muestra su valor con contexto.
    """
    resultado = analizar_licitacion()

    # Navegar por el diccionario usando la ruta del campo
    partes = campo.split(".")
    valor = resultado
    encontrado = True
    for parte in partes:
        if isinstance(valor, dict) and parte in valor:
            valor = valor[parte]
        else:
            encontrado = False
            break

    if not encontrado:
        valor = "No indica"

    return render_template(
        "detalle.html",
        campo=campo,
        valor=valor,
        encontrado=encontrado,
    )


@bp_main.route("/analizar", methods=["POST"])
def analizar():
    """
    Recibe los archivos subidos (pliego y detalle del concurso),
    ejecuta el análisis y devuelve el JSON de resultados.
    """
    pliego_file = request.files.get("pliego")
    detalle_file = request.files.get("detalle")

    if not pliego_file:
        return jsonify({"error": "No se proporcionó el archivo del pliego."}), 400

    import tempfile
    import os

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        pliego_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        resultado = analizar_licitacion(tmp_path)
    finally:
        os.unlink(tmp_path)

    # Si se subió un detalle del concurso, registrar información pero no se puede leer (PDF escaneado)
    detalle_info = None
    if detalle_file:
        detalle_info = {
            "nombre": detalle_file.filename,
            "tamaño": detalle_file.content_length,
            "nota": "PDF escaneado: no se pudo extraer texto automáticamente.",
        }

    return jsonify({
        "exito": True,
        "resultado": resultado,
        "detalle_info": detalle_info,
    })


@bp_main.route("/descargar")
def descargar():
    """
    Genera el JSON de análisis y lo sirve como archivo descargable.
    """
    resultado_json = analizar_licitacion_json()

    buffer = io.BytesIO()
    buffer.write(resultado_json.encode("utf-8"))
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/json",
        as_attachment=True,
        download_name="analisis_licitacion.json",
    )