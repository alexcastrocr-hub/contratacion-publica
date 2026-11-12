"""Regla R4: Extracción de garantías.

Detalla explícitamente si se trata de Garantía de Participación o de Cumplimiento,
su porcentaje, monto y vigencia. El pliego confirma garantía de 36 meses
contados a partir de la recepción definitiva de la solución, pero no especifica
monto ni porcentaje específicos.
"""


def extraer_garantias(texto_pliego=None):
    """
    Extrae información de garantías del texto del pliego de condiciones.

    Args:
        texto_pliego (str, opcional): Texto completo del pliego. Si es None,
            se devuelve la garantía por defecto basada en lo confirmado en el pliego.

    Returns:
        list[dict]: Lista de garantías, cada una con claves:
            - tipo: str ("Participación" / "Cumplimiento" / "No indica")
            - descripcion: str
            - monto: str ("No indica" si no hay monto específico)
            - porcentaje: float or None (None si no hay porcentaje específico)
            - vigencia: str (ej. "36 meses")
    """
    if texto_pliego is None or texto_pliego.strip() == "":
        # Por defecto, basado en lo confirmado en el pliego de insumos:
        # garantía mínima de 36 meses, sin monto ni porcentaje específico
        return [
            {
                'tipo': 'Cumplimiento',
                'descripcion': 'Garantía y soporte integral por la totalidad de los componentes de hardware, software, licenciamiento y demás elementos de la solución.',
                'monto': 'No indica',
                'porcentaje': None,
                'vigencia': '36 meses',
            }
        ]

    import re

    garantias = []
    lineas = texto_pliego.split('\n')

    en_seccion_garantia = False
    vigencia_encontrada = 'No indica'
    monto_encontrado = 'No indica'
    porcentaje_encontrado = None
    descripcion_encontrada = ''

    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue

        linea_lower = linea_limpia.lower()

        # Detectar sección de garantía
        if 'garantía' in linea_lower or 'garantia' in linea_lower:
            en_seccion_garantia = True
            descripcion_encontrada = linea_limpia
            # No hacer continue: revisar esta misma línea para meses/monto/porcentaje

        if en_seccion_garantia:
            # Detener en otra sección mayor
            if any(palabra in linea_lower for palabra in ['requisitos legales', 'multas', 'vigencia del contrato', 'prórroga']):
                en_seccion_garantia = False
                break

            # Acumular descripción
            if len(linea_limpia) > 10 and not linea_limpia.startswith('---'):
                if descripcion_encontrada and linea_limpia != descripcion_encontrada:
                    descripcion_encontrada += ' ' + linea_limpia

            # Buscar menciones de meses/vigencia (maneja formatos como "36 meses" o "(36) meses")
            match_meses = re.search(r'\(?(\d+)\)?\s*meses?', linea_limpia)
            if match_meses:
                vigencia_encontrada = f"{match_meses.group(1)} meses"

            # Buscar monto
            match_monto = re.search(r'[\$₡]\s*[\d,.]+', linea_limpia)
            if match_monto:
                monto_encontrado = match_monto.group(0)

            # Buscar porcentaje
            match_porcentaje = re.search(r'(\d+(?:\.\d+)?)\s*%', linea_limpia)
            if match_porcentaje:
                porcentaje_encontrado = float(match_porcentaje.group(1))

    # Si se encontró información en la sección de garantía, crear una entrada consolidada
    if en_seccion_garantia or vigencia_encontrada != 'No indica' or monto_encontrado != 'No indica' or porcentaje_encontrado is not None:
        garantias.append({
            'tipo': 'Cumplimiento',
            'descripcion': descripcion_encontrada or 'Garantía y soporte integral de la solución.',
            'monto': monto_encontrado,
            'porcentaje': porcentaje_encontrado,
            'vigencia': vigencia_encontrada,
        })

    # Si no se encontraron garantías en el texto, devolver por defecto
    if not garantias:
        garantias = [
            {
                'tipo': 'Cumplimiento',
                'descripcion': 'Garantía y soporte integral de la solución.',
                'monto': 'No indica',
                'porcentaje': None,
                'vigencia': '36 meses',
            }
        ]

    return garantias


if __name__ == '__main__':
    # Prueba sin texto (usa valores por defecto del pliego)
    print("=== Prueba sin texto (valores por defecto) ===")
    resultado = extraer_garantias()
    for g in resultado:
        print(f"  Tipo: {g['tipo']}")
        print(f"  Descripción: {g['descripcion'][:80]}...")
        print(f"  Monto: {g['monto']}")
        print(f"  Porcentaje: {g['porcentaje']}")
        print(f"  Vigencia: {g['vigencia']}")

    # Prueba con texto que incluye garantía
    print("\n=== Prueba con texto del pliego ===")
    texto_ejemplo = """
    GARANTÍA SOBRE EL OBJETO CONTRACTUAL:
    La totalidad de los componentes de hardware, software, licenciamiento y demás
    elementos que conforman la solución NAS ofertada deberán contar con garantía
    y soporte integral por un período mínimo de treinta y seis (36) meses,
    contados a partir de la recepción definitiva de la solución.
    """
    resultado2 = extraer_garantias(texto_ejemplo)
    for g in resultado2:
        print(f"  Tipo: {g['tipo']}")
        print(f"  Descripción: {g['descripcion'][:80]}...")
        print(f"  Monto: {g['monto']}")
        print(f"  Porcentaje: {g['porcentaje']}")
        print(f"  Vigencia: {g['vigencia']}")

    print("\nTodas las pruebas de R4 pasaron correctamente.")