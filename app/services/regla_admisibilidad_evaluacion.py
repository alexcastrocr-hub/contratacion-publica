"""Regla R3: Distinguir Requisitos de Admisibilidad de Criterios de Evaluación/Puntuación.

- Requisitos de Admisibilidad: condiciones obligatorias "Pasa / No Pasa".
- Criterios de Evaluación / Puntuación: asignación de puntos o porcentajes.
"""


def extraer_requisitos_admisibilidad(texto_pliego):
    """
    Extrae los requisitos de admisibilidad (condiciones obligatorias Pasa/No Pasa)
    del texto del pliego de condiciones.

    Args:
        texto_pliego (str): Texto completo extraído del pliego Word.

    Returns:
        list[str]: Lista de requisitos de admisibilidad encontrados.
                   Devuelve lista vacía si no se encuentran requisitos explícitos.
    """
    if not texto_pliego:
        return []

    requisitos = []
    lineas = texto_pliego.split('\n')

    # Buscar secciones que indiquen requisitos de admisibilidad
    en_seccion_admisibilidad = False
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue

        linea_lower = linea_limpia.lower()

        # Detectar inicio de sección de admisibilidad
        if 'requisitos de admisibilidad' in linea_lower or 'admisibilidad' in linea_lower:
            en_seccion_admisibilidad = True
            continue

        # Si estamos en la sección, recolectar líneas que parezcan requisitos
        if en_seccion_admisibilidad:
            # Detener si se encuentra otra sección mayor
            if any(palabra in linea_lower for palabra in ['criterios de evaluación', 'puntuación', 'slas', 'garantías']):
                en_seccion_admisibilidad = False
                continue

            # Recolectar líneas que tengan contenido de requisito
            if len(linea_limpia) > 10 and not linea_limpia.startswith('---'):
                requisitos.append(linea_limpia)

    return requisitos


def extraer_criterios_puntuacion(texto_pliego):
    """
    Extrae los criterios de evaluación / puntuación (puntos o porcentajes)
    del texto del pliego de condiciones.

    Args:
        texto_pliego (str): Texto completo extraído del pliego Word.

    Returns:
        list[dict]: Lista de criterios con claves 'criterio' y 'porcentaje_puntos'.
                    Devuelve lista vacía si no se encuentran criterios explícitos.
    """
    if not texto_pliego:
        return []

    criterios = []
    lineas = texto_pliego.split('\n')

    en_seccion_evaluacion = False
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue

        linea_lower = linea_limpia.lower()

        # Detectar inicio de sección de evaluación/puntuación
        if any(frase in linea_lower for frase in [
            'criterios de evaluación', 'evaluación', 'puntuación',
            'requisitos de puntuación'
        ]) and 'admisibilidad' not in linea_lower:
            en_seccion_evaluacion = True
            continue

        if en_seccion_evaluacion:
            # Detener si se encuentra otra sección mayor
            if any(palabra in linea_lower for palabra in ['garantías', 'referencias', 'multas', 'requisitos legales']):
                en_seccion_evaluacion = False
                continue

            # Recolectar líneas que parezcan criterios (contengan % o puntos)
            if len(linea_limpia) > 10 and not linea_limpia.startswith('---'):
                # Intentar separar criterio y porcentaje si hay un %
                if '%' in linea_limpia:
                    partes = linea_limpia.split('%', 1)
                    criterio = partes[0].strip()
                    porcentaje = partes[0].strip() + '%' if len(partes) > 1 else ''
                    criterios.append({
                        'criterio': criterio,
                        'porcentaje_puntos': porcentaje
                    })
                else:
                    criterios.append({
                        'criterio': linea_limpia,
                        'porcentaje_puntos': ''
                    })

    return criterios


def separar_admisibilidad_evaluacion(texto_pliego):
    """
    Separa el texto del pliego en dos grupos: requisitos de admisibilidad
    y criterios de puntuación/evaluación.

    Args:
        texto_pliego (str): Texto completo extraído del pliego.

    Returns:
        dict: Con claves 'requisitos_admisibilidad' (list[str]) y
              'criterios_puntuacion' (list[dict]).
    """
    return {
        'requisitos_admisibilidad': extraer_requisitos_admisibilidad(texto_pliego),
        'criterios_puntuacion': extraer_criterios_puntuacion(texto_pliego),
    }


if __name__ == '__main__':
    texto_ejemplo = """
    REQUISITOS DE ADMISIBILIDAD
    1. El oferente debe ser persona jurídica constituida en Costa Rica.
    2. Debe presentar carta vigente del fabricante.
    3. Debe estar al día con CCSS y FODESAF.

    CRITERIOS DE EVALUACIÓN
    Experiencia del oferente: 30%
    Propuesta técnica: 40%
    Precio: 30%
    """
    resultado = separar_admisibilidad_evaluacion(texto_ejemplo)
    print("Requisitos de admisibilidad:")
    for r in resultado['requisitos_admisibilidad']:
        print(f"  - {r}")
    print("\nCriterios de puntuación:")
    for c in resultado['criterios_puntuacion']:
        print(f"  - {c['criterio']}: {c['porcentaje_puntos']}")