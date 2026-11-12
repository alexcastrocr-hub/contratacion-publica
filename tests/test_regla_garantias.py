"""Pruebas para la Regla R4: Garantías."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_garantias import extraer_garantias


def test_garantia_vigencia_36_meses_cifra_control():
    """R4: La garantía mínima confirmada en el pliego es 36 meses."""
    garantias = extraer_garantias()
    assert garantias[0]["vigencia"] == "36 meses"


def test_garantia_monto_no_indica():
    """R4: El pliego no especifica monto, debe ser 'No indica'."""
    garantias = extraer_garantias()
    assert garantias[0]["monto"] == "No indica"


def test_garantia_porcentaje_none():
    """R4: El pliego no especifica porcentaje, debe ser None."""
    garantias = extraer_garantias()
    assert garantias[0]["porcentaje"] is None


def test_garantia_tipo_cumplimiento():
    """R4: El tipo de garantía es Cumplimiento."""
    garantias = extraer_garantias()
    assert garantias[0]["tipo"] == "Cumplimiento"


def test_garantia_con_texto_pliego():
    """R4: Con texto del pliego que mencione 36 meses, se extrae correctamente."""
    texto = """
    GARANTÍA SOBRE EL OBJETO CONTRACTUAL:
    La totalidad de los componentes deberán contar con garantía y soporte integral
    por un período mínimo de treinta y seis (36) meses, contados a partir de la
    recepción definitiva de la solución.
    """
    garantias = extraer_garantias(texto)
    assert len(garantias) > 0
    assert garantias[0]["vigencia"] == "36 meses"


def test_garantia_caso_limite_sin_texto():
    """Caso límite: sin texto de pliego, se usan valores por defecto (36 meses)."""
    garantias = extraer_garantias(None)
    assert garantias[0]["vigencia"] == "36 meses"