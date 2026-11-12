"""Pruebas para la Regla R2: Cálculo de presupuesto en USD."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_presupuesto_usd import calcular_presupuesto_usd


def test_calculo_presupuesto_usd_cifra_control():
    """R2: 1,000,000 CRC / 500 = 2000.0 USD (cifra de control del plan)."""
    resultado = calcular_presupuesto_usd(1000000, 500)
    assert resultado == 2000.0


def test_calculo_presupuesto_usd_redondeo_2_decimales():
    """R2: El resultado se redondea a 2 decimales."""
    resultado = calcular_presupuesto_usd(1000001, 500)
    assert resultado == 2000.0  # 2000.002 redondeado a 2000.0


def test_calculo_presupuesto_usd_con_none_crc():
    """R2: Si presupuesto_crc es None, devuelve None."""
    assert calcular_presupuesto_usd(None, 500) is None


def test_calculo_presupuesto_usd_con_none_tipo_cambio():
    """R2: Si tipo_cambio_bccr es None, devuelve None."""
    assert calcular_presupuesto_usd(1000000, None) is None


def test_calculo_presupuesto_usd_con_tipo_cambio_cero():
    """R2: Si tipo_cambio_bccr es 0, devuelve None (evita división por cero)."""
    assert calcular_presupuesto_usd(1000000, 0) is None


def test_calculo_presupuesto_usd_caso_limite_sin_monto_crc():
    """Caso límite: presupuesto sin monto en CRC -> presupuesto_usd es None."""
    assert calcular_presupuesto_usd(None, 530.45) is None


def test_calculo_presupuesto_usd_caso_limite_sin_tipo_cambio():
    """Caso límite: tipo de cambio BCCR no disponible -> presupuesto_usd es None."""
    assert calcular_presupuesto_usd(500000000, None) is None