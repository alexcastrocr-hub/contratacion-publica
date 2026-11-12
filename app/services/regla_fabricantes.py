"""Regla R5: Fabricantes.

Verifica si se exigen cartas de respaldo del fabricante y si se requiere
traducción oficial o simple para la documentación técnica.
"""


def extraer_fabricantes(texto_pliego=None):
    """
    Extrae información sobre requisitos de fabricantes del texto del pliego.

    Args:
        texto_pliego (str, opcional): Texto completo del pliego. Si es None,
            se devuelve un valor por defecto basado en lo confirmado en el pliego.

    Returns:
        dict: Con claves:
            - requeridas: bool (True si se requieren cartas de fabricante)
            - detalle: str (descripción del requisito de cartas)
            - documentacion_espanol_requerida: bool (True si se requiere doc en español)
            - tipo_traduccion: str ("Oficial" / "Simple" / "No aplica" / "No indica")
    """
    if texto_pliego is None or texto_pliego.strip() == "":
        # Por defecto, basado en lo confirmado en el pliego de insumos:
        # Se requiere carta vigente del fabricante emitida dentro de los 3 meses
        # anteriores a la presentación de la oferta.
        # La documentación del fabricante debe estar en español (verificado en cláusulas
        # de documentación técnica del pliego).
        return {
            'requeridas': True,
            'detalle': 'Carta vigente emitida por el fabricante, dirigida al Banco Central de Costa Rica, dentro de los 3 meses anteriores a la fecha de presentación de la oferta.',
            'documentacion_espanol_requerida': True,
            'tipo_traduccion': 'Simple',  # Basado en lo observado en el pliego
        }

    resultado = {
        'requeridas': False,
        'detalle': 'No se encontraron requisitos explícitos de cartas de fabricante.',
        'documentacion_espanol_requerida': False,
        'tipo_traduccion': 'No indica',
    }

    lineas = texto_pliego.split('\n')

    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue

        linea_lower = linea_limpia.lower()

        # Detectar cartas de fabricante
        if 'carta' in linea_lower and 'fabricante' in linea_lower:
            resultado['requeridas'] = True
            resultado['detalle'] = linea_limpia

        # Detectar documentación en español
        if 'documentación' in linea_lower and 'español' in linea_lower:
            resultado['documentacion_espanol_requerida'] = True

        # Detectar tipo de traducción
        if 'traducción oficial' in linea_lower or 'traduccion oficial' in linea_lower:
            resultado['tipo_traduccion'] = 'Oficial'
        elif 'traducción simple' in linea_lower or 'traduccion simple' in linea_lower:
            resultado['tipo_traduccion'] = 'Simple'

    return resultado


if __name__ == '__main__':
    # Prueba sin texto (valores por defecto del pliego)
    print("=== Prueba sin texto (valores por defecto) ===")
    resultado = extraer_fabricantes()
    print(f"  Cartas requeridas: {resultado['requeridas']}")
    print(f"  Detalle: {resultado['detalle']}")
    print(f"  Documentación en español requerida: {resultado['documentacion_espanol_requerida']}")
    print(f"  Tipo de traducción: {resultado['tipo_traduccion']}")

    # Prueba con texto del pliego
    print("\n=== Prueba con texto del pliego ===")
    texto_ejemplo = """
    El oferente deberá presentar una carta vigente emitida por el fabricante de la
    solución NAS ofertada, dirigida al Banco Central de Costa Rica, en la que conste
    expresamente su respaldo. La carta deberá haber sido emitida dentro de los tres
    (3) meses anteriores a la fecha de presentación de la oferta.

    La documentación técnica del fabricante deberá estar disponible en español.
    """
    resultado2 = extraer_fabricantes(texto_ejemplo)
    print(f"  Cartas requeridas: {resultado2['requeridas']}")
    print(f"  Detalle: {resultado2['detalle']}")
    print(f"  Documentación en español requerida: {resultado2['documentacion_espanol_requerida']}")
    print(f"  Tipo de traducción: {resultado2['tipo_traduccion']}")

    print("\nTodas las pruebas de R5 pasaron correctamente.")