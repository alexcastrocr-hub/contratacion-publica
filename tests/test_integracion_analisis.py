"""Pruebas de integración: análisis completo de licitación en modo fallback."""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.agente_ia import analizar_licitacion_json, analizar_licitacion


def test_analisis_devuelve_json_valido():
    """Integración: El análisis devuelve un JSON válido serializable."""
    json_str = analizar_licitacion_json()
    datos = json.loads(json_str)
    assert isinstance(datos, dict)


def test_json_tiene_todos_los_bloques_requeridos():
    """Integración: El JSON tiene todos los bloques definidos en el contrato de AGENTS.md."""
    datos = analizar_licitacion()
    bloques_requeridos = [
        "identificacion_concurso",
        "datos_financieros",
        "gestion_contacto",
        "alcance_general",
        "cronograma",
        "esquema_participacion",
        "garantias",
        "criterios_evaluacion_requisitos",
        "condiciones_ejecutivas",
    ]
    for bloque in bloques_requeridos:
        assert bloque in datos, f"Falta el bloque {bloque} en el JSON de salida"


def test_campos_ausentes_devuelven_no_indica():
    """Caso límite: Campos que no están en los insumos devuelven 'No indica' o null."""
    datos = analizar_licitacion()

    # Campos que probablemente están en el PDF escaneado (no legible)
    assert datos["identificacion_concurso"]["numero_licitacion"] == "No indica"
    assert datos["identificacion_concurso"]["tipo_licitacion"] == "No indica"
    assert datos["identificacion_concurso"]["tipo_concurso"] == "No indica"

    # Presupuesto sin monto -> None
    assert datos["datos_financieros"]["presupuesto_crc"] is None
    assert datos["datos_financieros"]["tipo_cambio_bccr"] is None
    assert datos["datos_financieros"]["presupuesto_usd"] is None

    # Fechas clave no disponibles
    assert datos["cronograma"]["fecha_publicacion"] == "No indica"
    assert datos["cronograma"]["fecha_apertura"] == "No indica"
    assert datos["cronograma"]["fecha_limite_presentacion"] == "No indica"


def test_garantia_36_meses_en_json():
    """Cifra de control: La garantía en el JSON tiene vigencia de 36 meses."""
    datos = analizar_licitacion()
    assert len(datos["garantias"]) > 0
    assert datos["garantias"][0]["vigencia"] == "36 meses"


def test_cartas_fabricante_requeridas_en_json():
    """Cifra de control: Las cartas de fabricante son requeridas."""
    datos = analizar_licitacion()
    assert datos["criterios_evaluacion_requisitos"]["cartas_fabricante"]["requeridas"] is True