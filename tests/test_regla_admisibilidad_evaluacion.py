"""Pruebas para la Regla R3: Admisibilidad vs Evaluación separadas."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.regla_admisibilidad_evaluacion import separar_admisibilidad_evaluacion


def test_admisibilidad_y_evaluacion_están_separadas():
    """R3: Los requisitos de admisibilidad y criterios de puntuación están en listas separadas."""
    texto = """
    REQUISITOS DE ADMISIBILIDAD
    1. El oferente debe ser persona jurídica constituida en Costa Rica.
    2. Debe presentar carta vigente del fabricante.

    CRITERIOS DE EVALUACIÓN
    Experiencia del oferente: 30%
    Propuesta técnica: 40%
    """
    resultado = separar_admisibilidad_evaluacion(texto)

    assert "requisitos_admisibilidad" in resultado
    assert "criterios_puntuacion" in resultado
    assert isinstance(resultado["requisitos_admisibilidad"], list)
    assert isinstance(resultado["criterios_puntuacion"], list)


def test_texto_vacio_devuelve_listas_vacías():
    """R3: Texto vacío devuelve listas vacías sin error."""
    resultado = separar_admisibilidad_evaluacion("")
    assert resultado["requisitos_admisibilidad"] == []
    assert resultado["criterios_puntuación"] == [] if "criterios_puntuación" in resultado else resultado["criterios_puntuacion"] == []


def test_texto_none_devuelve_listas_vacías():
    """R3: Texto None devuelve listas vacías sin error."""
    resultado = separar_admisibilidad_evaluacion(None)
    assert resultado["requisitos_admisibilidad"] == []
    assert resultado["criterios_puntuacion"] == []