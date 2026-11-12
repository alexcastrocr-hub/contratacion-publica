"""Pruebas para la Regla R1: Valor por defecto para datos ausentes."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_valor_por_defecto import valor_por_defecto, campo_en_datos


def test_valor_por_defecto_con_valor_valido():
    """R1: Un valor válido se devuelve tal cual."""
    assert valor_por_defecto("Licitación Mayor") == "Licitación Mayor"


def test_valor_por_defecto_con_none():
    """R1: None devuelve 'No indica'."""
    assert valor_por_defecto(None) == "No indica"


def test_valor_por_defecto_con_string_vacio():
    """R1: String vacío devuelve 'No indica'."""
    assert valor_por_defecto("") == "No indica"


def test_valor_por_defecto_con_solo_espacios():
    """R1: String con solo espacios devuelve 'No indica'."""
    assert valor_por_defecto("   ") == "No indica"


def test_valor_por_defecto_con_numero():
    """R1: Un número se devuelve tal cual."""
    assert valor_por_defecto(1000000) == 1000000


def test_valor_por_defecto_con_booleano():
    """R1: Un booleano se devuelve tal cual."""
    assert valor_por_defecto(True) is True
    assert valor_por_defecto(False) is False


def test_campo_en_datos_con_clave_existente():
    """R1: Clave existente en diccionario devuelve su valor."""
    datos = {"numero_licitacion": "2026LN-001"}
    assert campo_en_datos(datos, "numero_licitacion") == "2026LN-001"


def test_campo_en_datos_con_clave_inexistente():
    """R1: Clave inexistente devuelve 'No indica'."""
    datos = {"numero_licitacion": "2026LN-001"}
    assert campo_en_datos(datos, "tipo_licitacion") == "No indica"


def test_campo_en_datos_con_valor_none():
    """R1: Clave con valor None devuelve 'No indica'."""
    datos = {"presupuesto": None}
    assert campo_en_datos(datos, "presupuesto") == "No indica"


def test_campo_en_datos_con_diccionario_none():
    """R1: Diccionario None devuelve 'No indica' para cualquier clave."""
    assert campo_en_datos(None, "cualquier_cosa") == "No indica"