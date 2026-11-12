"""Pruebas para la Regla R5: Fabricantes."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_fabricantes import extraer_fabricantes


def test_cartas_fabricante_requeridas():
    """R5: Las cartas de fabricante son requeridas (True)."""
    resultado = extraer_fabricantes()
    assert resultado["requeridas"] is True


def test_documentacion_espanol_requerida():
    """R5: La documentación en español es requerida."""
    resultado = extraer_fabricantes()
    assert resultado["documentacion_espanol_requerida"] is True


def test_tipo_traduccion_simple():
    """R5: El tipo de traducción es Simple."""
    resultado = extraer_fabricantes()
    assert resultado["tipo_traduccion"] == "Simple"


def test_detalle_cartas_no_vacio():
    """R5: El detalle de las cartas no está vacío."""
    resultado = extraer_fabricantes()
    assert resultado["detalle"] != ""
    assert "fabricante" in resultado["detalle"].lower()


def test_fabricantes_con_texto_pliego():
    """R5: Con texto del pliego que mencione carta de fabricante, se detecta."""
    texto = """
    El oferente deberá presentar una carta vigente emitida por el fabricante
    de la solución NAS ofertada, dirigida al Banco Central de Costa Rica.
    """
    resultado = extraer_fabricantes(texto)
    assert resultado["requeridas"] is True