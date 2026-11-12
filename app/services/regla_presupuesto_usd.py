"""Regla R2: Cálculo de presupuesto en USD.

Identifica el Presupuesto Estimado en Colones Costa-ricenses (CRC).
Utiliza el Tipo de Cambio de Venta oficial del BCCR.
Calcula: presupuesto_usd = presupuesto_crc / tipo_cambio_bccr.
Redondea el resultado a 2 decimales.
"""


def calcular_presupuesto_usd(presupuesto_crc, tipo_cambio_bccr):
    """
    Calcula el presupuesto en dólares dividiendo CRC por el tipo de cambio BCCR.

    Args:
        presupuesto_crc (float or int or None): Presupuesto en colones costarricenses.
        tipo_cambio_bccr (float or int or None): Tipo de cambio de venta del BCCR.

    Returns:
        float: Presupuesto en USD redondeado a 2 decimales.
        None: Si alguno de los parámetros es None o cero (no se puede calcular).
    """
    if presupuesto_crc is None or tipo_cambio_bccr is None:
        return None
    if tipo_cambio_bccr == 0:
        return None
    try:
        resultado = float(presupuesto_crc) / float(tipo_cambio_bccr)
        return round(resultado, 2)
    except (ValueError, TypeError):
        return None


if __name__ == '__main__':
    # Prueba rápida de la regla R2
    print(f"1,000,000 CRC / 500 = {calcular_presupuesto_usd(1000000, 500)} USD")
    print(f"None CRC / 500 = {calcular_presupuesto_usd(None, 500)} USD")
    print(f"1,000,000 CRC / None = {calcular_presupuesto_usd(1000000, None)} USD")
    print(f"1,000,000 CRC / 0 = {calcular_presupuesto_usd(1000000, 0)} USD")