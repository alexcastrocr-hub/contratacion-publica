"""Pruebas para casos límite definidos en AGENTS.md."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_valor_por_defecto import valor_por_defecto, campo_en_datos
from app.services.regla_presupuesto_usd import calcular_presupuesto_usd
from app.services.regla_garantias import extraer_garantias


def test_caso_limite_pdf_escanedo_sin_texto():
    """Caso límite: PDF escaneado sin texto -> campos como 'No indica'."""
    # Simula que el PDF no tiene texto extraíble
    texto_pdf = ""
    resultado = campo_en_datos({"numero_licitacion": texto_pdf or None}, "numero_licitacion")
    assert resultado == "No indica"


def test_caso_limite_campo_ausente_en_ambos_documentos():
    """Caso límite: Campo ausente en ambos documentos -> 'No indica' o null."""
    datos = {"otro_campo": "valor"}
    assert campo_en_datos(datos, "numero_licitacion") == "No indica"


def test_caso_limite_presupuesto_sin_monto_crc():
    """Caso límite: Presupuesto sin monto en CRC -> presupuesto_crc y presupuesto_usd son None."""
    assert calcular_presupuesto_usd(None, 500) is None
    assert calcular_presupuesto_usd(None, None) is None


def test_caso_limite_tipo_cambio_bccr_no_disponible():
    """Caso límite: Tipo de cambio BCCR no disponible -> presupuesto_usd es None."""
    assert calcular_presupuesto_usd(1000000, None) is None


def test_caso_limite_garantia_sin_monto_ni_porcentaje():
    """Caso límite: Garantía sin monto ni porcentaje -> monto='No indica', porcentaje=None."""
    garantias = extraer_garantias()
    assert garantias[0]["monto"] == "No indica"
    assert garantias[0]["porcentaje"] is None


def test_caso_limite_oferta_en_conjunto_vs_consorcio():
    """Caso límite: El pliego menciona consorcio pero no oferta en conjunto separada."""
    # La regla de negocio establece que oferta_en_conjunto se devuelve como false/null
    # hasta confirmar si aplica (no está en el pliego Word)
    from app.services.agente_ia import analizar_licitacion
    datos = analizar_licitacion()
    assert datos["esquema_participacion"]["oferta_en_conjunto"] is False
    assert datos["esquema_participacion"]["consorcio"]["aplica"] is False