"""Regla R1: Valor por defecto para datos ausentes.

Si un campo no se encuentra explícitamente en los insumos, se asigna "No indica"
(texto) o null (JSON). Nunca se rellena con suposiciones.
"""


def valor_por_defecto(valor):
    """
    Devuelve el valor si existe, o "No indica" si el campo está ausente.

    Args:
        valor: Valor extraído de los insumos (str, int, float, bool, None, etc.)

    Returns:
        El valor original si no es None ni string vacío; de lo contrario, "No indica".
    """
    if valor is None:
        return "No indica"
    if isinstance(valor, str) and valor.strip() == "":
        return "No indica"
    return valor


def campo_en_datos(datos, clave):
    """
    Busca una clave en un diccionario de datos extraídos y aplica la regla R1.

    Args:
        datos (dict): Diccionario con los datos extraídos de los insumos.
        clave (str): Clave a buscar en el diccionario.

    Returns:
        El valor asociado a la clave si existe y no está vacío; "No indica" en caso contrario.
    """
    if datos is None:
        return "No indica"
    if clave not in datos:
        return "No indica"
    return valor_por_defecto(datos[clave])