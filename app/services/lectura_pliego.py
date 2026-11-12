"""Servicio para leer el pliego de condiciones (.docx) y extraer texto y tablas."""

from docx import Document


def extraer_pliego(ruta_archivo=None):
    """
    Extrae todo el contenido (párrafos y tablas) de un documento Word del pliego de condiciones.

    Args:
        ruta_archivo (str, opcional): Ruta al archivo .docx. Si no se proporciona,
            se usa la ruta por defecto en la carpeta insumos.

    Returns:
        dict: Diccionario con las claves:
            - 'texto': str con todo el texto concatenado (párrafos y tablas)
            - 'parrafos': lista de str con cada párrafo no vacío
            - 'tablas': lista de tablas, cada tabla es una lista de filas (lista de celdas)
            - 'numero_tablas': int con la cantidad de tablas encontradas
            - 'ruta': str con la ruta del archivo leído
    """
    if ruta_archivo is None:
        ruta_archivo = 'insumos/PLIEGO DE CONDICIONES ALMACENAMIENTO NAS MODIFICADO.docx'

    doc = Document(ruta_archivo)

    parrafos = []
    for p in doc.paragraphs:
        if p.text.strip():
            parrafos.append(p.text)

    tablas = []
    for tabla in doc.tables:
        filas = []
        for fila in tabla.rows:
            celdas = [celda.text.strip() for celda in fila.cells]
            filas.append(celdas)
        if filas:
            tablas.append(filas)

    texto_completo = '\n'.join(parrafos)
    for tabla in tablas:
        for fila in tabla:
            texto_completo += '\n' + ' | '.join(fila)

    return {
        'texto': texto_completo,
        'parrafos': parrafos,
        'tablas': tablas,
        'numero_tablas': len(tablas),
        'ruta': ruta_archivo,
    }


if __name__ == '__main__':
    resultado = extraer_pliego()
    print(f"Archivo leído: {resultado['ruta']}")
    print(f"Párrafos: {len(resultado['parrafos'])}")
    print(f"Tablas: {resultado['numero_tablas']}")
    print(f"Primeros 200 caracteres de texto:\n{resultado['texto'][:200]}")