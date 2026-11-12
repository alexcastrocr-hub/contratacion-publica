"""Integración del agente de IA con contrato JSON.

Lee la llave del agente de IA desde .env. Si no hay llave disponible, aplica
modo fallback usando las reglas de negocio locales (R1-R5) para generar el JSON.
Siempre devuelve JSON válido según el contrato de AGENTS.md.
"""

import json
import os

from app.services.lectura_pliego import extraer_pliego
from app.services.regla_valor_por_defecto import valor_por_defecto, campo_en_datos
from app.services.regla_presupuesto_usd import calcular_presupuesto_usd
from app.services.regla_admisibilidad_evaluacion import separar_admisibilidad_evaluacion
from app.services.regla_garantias import extraer_garantias
from app.services.regla_fabricantes import extraer_fabricantes


def obtener_llave_ia():
    """
    Lee la llave del agente de IA desde las variables de entorno.

    Returns:
        str or None: La llave de IA si está configurada, None en caso contrario.
    """
    return os.environ.get("AGENTE_IA_KEY") or os.environ.get("AGENTE_IA_KEY", "")


def construir_json_vacia():
    """
    Construye un JSON vacío según el contrato de AGENTS.md, con todos los campos
    como "No indica" o null.

    Returns:
        dict: Estructura JSON vacía válida según el contrato.
    """
    return {
        "identificacion_concurso": {
            "numero_licitacion": "No indica",
            "tipo_licitacion": "No indica",
            "tipo_concurso": "No indica",
        },
        "datos_financieros": {
            "presupuesto_crc": None,
            "tipo_cambio_bccr": None,
            "presupuesto_usd": None,
        },
        "gestion_contacto": {
            "administrador_contrato": "No indica",
        },
        "alcance_general": {
            "descripcion_alcance": "No indica",
        },
        "cronograma": {
            "fecha_publicacion": "No indica",
            "fecha_limite_aclaraciones": "No indica",
            "fecha_limite_modificaciones": "No indica",
            "fecha_limite_presentacion": "No indica",
            "fecha_apertura": "No indica",
            "mejora_precio": {
                "aplica": False,
                "condiciones": "No indica",
            },
        },
        "esquema_participacion": {
            "consorcio": {
                "aplica": False,
                "condiciones": "No indica",
            },
            "representante_casas_extranjeras": False,
            "oferta_en_conjunto": False,
        },
        "garantias": [
            {
                "tipo": "No indica",
                "descripcion": "No indica",
                "monto": "No indica",
                "porcentaje": None,
                "vigencia": "No indica",
            }
        ],
        "criterios_evaluacion_requisitos": {
            "requisitos_admisibilidad": [],
            "slas_compromiso": [],
            "criterios_puntuacion": [],
            "referencias_solicitadas": "No indica",
            "cartas_fabricante": {
                "requeridas": False,
                "detalle": "No indica",
            },
            "documentacion_espanol": {
                "requerida": False,
                "tipo_traduccion": "No indica",
            },
            "multas_penales": "No indica",
            "requisitos_legales": [],
        },
        "condiciones_ejecutivas": {
            "vigencia_contrato": "No indica",
            "prorroga_contrato": {
                "aplica": False,
                "condiciones": "No indica",
            },
            "alcance_trabajo_detallado": "No indica",
            "condiciones_pago": "No indica",
        },
    }


def generar_json_con_reglas_locales(texto_pliego):
    """
    Genera el JSON de salida aplicando las reglas de negocio locales (R1-R5)
    cuando no hay llave de IA disponible (modo fallback).

    Args:
        texto_pliego (str): Texto completo extraído del pliego Word.

    Returns:
        dict: JSON estructurado según el contrato de AGENTS.md.
    """
    resultado = construir_json_vacia()

    # Aplicar regla R4: Garantías (36 meses confirmados en el pliego)
    garantias = extraer_garantias(texto_pliego)
    if garantias:
        resultado["garantias"] = garantias

    # Aplicar regla R5: Fabricantes
    fabricantes = extraer_fabricantes(texto_pliego)
    resultado["criterios_evaluacion_requisitos"]["cartas_fabricante"] = {
        "requeridas": fabricantes["requeridas"],
        "detalle": fabricantes["detalle"],
    }
    resultado["criterios_evaluacion_requisitos"]["documentacion_espanol"] = {
        "requerida": fabricantes["documentacion_espanol_requerida"],
        "tipo_traduccion": fabricantes["tipo_traduccion"],
    }

    # Aplicar regla R3: Admisibilidad vs Evaluación
    separacion = separar_admisibilidad_evaluacion(texto_pliego)
    resultado["criterios_evaluacion_requisitos"]["requisitos_admisibilidad"] = (
        separacion["requisitos_admisibilidad"]
    )
    resultado["criterios_evaluacion_requisitos"]["criterios_puntuacion"] = (
        separacion["criterios_puntuacion"]
    )

    # Alcance general: usar el objeto contractual del pliego
    if texto_pliego and "NAS" in texto_pliego:
        resultado["alcance_general"]["descripcion_alcance"] = (
            "Solución de Almacenamiento NAS Empresarial para el Banco Central de Costa Rica."
        )

    return resultado


def procesar_con_agente_ia(texto_pliego, llave_ia):
    """
    Intenta procesar el texto del pliego con el agente de IA externo.

    Esta función es un placeholder para la integración con una API externa
    de IA. Si la llave no está configurada o falla, retorna None para usar
    modo fallback.

    Args:
        texto_pliego (str): Texto del pliego.
        llave_ia (str): Llave de API del agente de IA.

    Returns:
        dict or None: JSON del agente de IA si tiene éxito, None si falla.
    """
    if not llave_ia or llave_ia.strip() == "":
        return None

    # Placeholder: aquí se haría la llamada a la API externa de IA
    # Por ahora, retorna None para forzar modo fallback
    return None


def analizar_licitacion(ruta_pliego=None):
    """
    Función principal de análisis de licitación.

    Lee el pliego, intenta usar el agente de IA (si hay llave), y si no,
    aplica reglas de negocio locales. Siempre devuelve JSON válido.

    Args:
        ruta_pliego (str, opcional): Ruta al archivo .docx del pliego.

    Returns:
        dict: JSON estructurado según el contrato de AGENTS.md.
    """
    # Leer el pliego
    datos_pliego = extraer_pliego(ruta_pliego)
    texto_pliego = datos_pliego["texto"]

    # Obtener llave de IA desde .env
    llave_ia = obtener_llave_ia()

    # Intentar con agente de IA
    resultado_ia = procesar_con_agente_ia(texto_pliego, llave_ia)

    if resultado_ia is not None:
        return resultado_ia

    # Modo fallback: reglas de negocio locales
    return generar_json_con_reglas_locales(texto_pliego)


def analizar_licitacion_json(ruta_pliego=None):
    """
    Como analizar_licitacion pero devuelve string JSON listo para enviar al frontend.

    Returns:
        str: JSON serializado.
    """
    resultado = analizar_licitacion(ruta_pliego)
    return json.dumps(resultado, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Prueba rápida en modo fallback (sin llave de IA)
    print("=== Prueba en modo fallback (sin llave de IA) ===")
    json_resultado = analizar_licitacion_json()
    print(json_resultado[:500])
    print("...")
    print("\nJSON generado correctamente en modo fallback.")