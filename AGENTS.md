# AGENTS.md

## Qué es esta app

Aplicación tipo Analista Virtual de Contratación Pública para el marco de contratación administrativa de Costa Rica (plataforma SICOP, Banco Central de Costa Rica - BCCR). Su función es procesar dos documentos de entrada (Pliego de Condiciones / Cartel y Detalle del Concurso) y extraer información estructurada de una licitación pública, respetando estrictamente los datos oficiales sin inventar ni asumir información.

El resultado de la extracción se devuelve en formato JSON válido según el esquema definido en este documento.

## Datos de entrada

### Archivos de insumos (carpeta `insumos/` — no modificar)

| # | Nombre real del archivo | Tipo | Filas / Columnas | ¿Tiene texto extraíble? | De qué trata |
|---|-------------------------|------|------------------|------------------------|--------------|
| 1 | `PLIEGO DE CONDICIONES ALMACENAMIENTO NAS MODIFICADO.docx` | Word (.docx) | 1032 párrafos; 14 tablas (tamaños variables: 2x2, 5x5, 4x2, 5x5, 3x5, 3x8, 9x2, 5x3, 12x4, 18x5, 18x2, 1x3, 3x2, 2x3) | Sí (texto extraíble) | Pliego de condiciones para la contratación de bienes y servicios: **Solución de Almacenamiento NAS Empresarial** para el Banco Central de Costa Rica. Incluye objeto contractual, arquitectura general, alta disponibilidad, distribución en dos centros de datos del BCCR, garantía y soporte, SLAs, requisitos de admisibilidad, estructura de precio, tipos de cambio BCCR, consorcio, requisitos legales, multas y cláusulas penales, vigencia del contrato, alcance del trabajo y condiciones de pago. |
| 2 | `DETALLE CONCURSO.pdf` | PDF | 4 páginas | **No** (PDF escaneado, 0 caracteres de texto extraíble en las 4 páginas) | No se pudo leer su contenido. Probablemente contiene datos generales del concurso (número de licitación, tipo, presupuesto, fechas clave, etc.), pero al estar escaneado no es posible confirmar qué campos incluye. |

### Campos identificados en el pliego de insumos (Word)

- Objeto contractual: Solución de almacenamiento NAS empresarial para el BCCR
- Período estimado de la contratación
- Modalidad de la contratación
- Disponibilidad presupuestaria
- Detalle del renglón o los renglones
- Arquitectura general requerida (NAS empresarial, 2 centros de datos del BCCR, alta disponibilidad)
- Garantía sobre el objeto contractual: mínimo 36 meses contados a partir de la recepción definitiva
- Tipo de cambio de venta de referencia vigente a la fecha de apertura (BCCR)
- Ofertas en consorcio (SICOP, número de consorcio, responsabilidad solidaria)
- Requisitos de admisibilidad (carta vigente del fabricante, emitida dentro de los 3 meses anteriores a la presentación)
- SLAs / tiempos de restauración por severidad de incidente
- Estructura de precio (costos directos, indirectos, utilidad, imprevistos; monedas; reajuste)
- Multas y sanciones por incumplimiento
- Requisitos legales
- Administrador del Contrato (referido en cláusulas de revisión de precios y cronograma)
- Vigencia del contrato y prórrogas al plazo de ejecución
- Alcance del trabajo (actividades, cantidades, avance físico por mes)
- Condiciones de pago (orden de inicio, cronograma de pagos)

### Campos del contexto que NO aparecen confirmados en los insumos disponibles

Los siguientes campos mencionados en `Contexto_Mi_App.md` no se pudieron localizar en el pliego Word ni en el PDF escaneado:

- Número de Licitación
- Tipo de Licitación
- Tipo de Concurso
- Presupuesto Estimado (monto en CRC / USD)
- Fecha de Publicación
- Fecha de Apertura
- Fecha Límite Aclaraciones
- Fecha Límite Modificaciones
- Fecha Límite Presentación
- Mejora de Precio
- Esquema General
- Representante Casa Extranjeras
- Oferta en Conjunto
- Monto de Garantía (solo se confirma garantía de 36 meses, no el monto)
- Porcentaje de Garantía (%)
- Requisitos de Puntuación / Evaluación
- Información de Referencias Solicitadas
- Documentación del Fabricante en Español
- Condiciones de Pago específicas (plazos, facturación, hitos)

**Nota:** Es probable que estos campos estén en `DETALLE CONCURSO.pdf`, pero al ser un PDF escaneado no se pudo verificar. Se marcarán como `"No indica"` o `null` en la salida del agente hasta que se cuente con una versión legible del PDF.

## Reglas de negocio (código, sin IA)

1. **Extracción exclusivamente de documentos**: Toda la información debe provenir de los dos archivos de insumos. No se asume ni se inventa ningún dato.

2. **Valor por defecto para datos ausentes**: Si un campo no se encuentra explícitamente en el pliego o en el detalle del concurso, se asigna `"No indica"` (texto) o `null` (JSON). Nunca se rellena con suposiciones.

3. **Cálculo de presupuesto en USD**:
   - Se identifica el Presupuesto Estimado en Colones Costa-ricenses (CRC).
   - Se utiliza el Tipo de Cambio de Venta oficial del BCCR correspondiente a la fecha de consulta.
   - Se calcula: `presupuesto_usd = presupuesto_crc / tipo_cambio_bccr`.
   - El resultado se redondea a 2 decimales.

4. **Distingue admisibilidad vs. evaluación**:
   - Requisitos de Admisibilidad: condiciones obligatorias "Pasa / No Pasa".
   - Criterios de Evaluación / Puntuación: asignación de puntos o porcentajes.

5. **Garantías**: Se detalla explícitamente si se trata de Garantía de Participación o de Cumplimiento, su porcentaje, monto y vigencia.

6. **Fabricantes**: Se verifica si se exigen cartas de respaldo y si se requiere traducción oficial o simple para la documentación técnica.

7. **Formato de salida**: Siempre JSON válido, sin texto decorativo adicional ni bloques fuera de la estructura.

8. **Sin uso de IA para reglas de negocio**: Estas reglas se aplican de forma determinista en el código de la aplicación; el agente de IA solo se encarga de la extracción de los documentos.

## Lo que hace el agente de IA (con el contrato JSON)

El agente de IA procesa el Pliego de Condiciones y el Detalle del Concurso y extrae la información estructurada respetando estrictamente los datos oficiales.

### Contrato JSON de salida

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AnalisisLicitacionPublicaCR",
  "type": "object",
  "properties": {
    "identificacion_concurso": {
      "type": "object",
      "properties": {
        "numero_licitacion": { "type": "string", "example": "2026LN-000001-XXXXX" },
        "tipo_licitacion": { "type": "string", "example": "Licitación Mayor / Licitación Menor / Reducida" },
        "tipo_concurso": { "type": "string", "example": "Nacional / Internacional" }
      },
      "required": ["numero_licitacion", "tipo_licitacion", "tipo_concurso"]
    },
    "datos_financieros": {
      "type": "object",
      "properties": {
        "presupuesto_crc": { "type": "number", "description": "Monto total del presupuesto en colones" },
        "tipo_cambio_bccr": { "type": "number", "description": "Tipo de cambio de venta del BCCR utilizado" },
        "presupuesto_usd": { "type": "number", "description": "Presupuesto recalculado en dólares (CRC / Tipo Cambio)" }
      },
      "required": ["presupuesto_crc", "tipo_cambio_bccr", "presupuesto_usd"]
    },
    "gestion_contacto": {
      "type": "object",
      "properties": {
        "administrador_contrato": { "type": "string", "description": "Nombre, unidad o departamento responsable" }
      }
    },
    "alcance_general": {
      "type": "object",
      "properties": {
        "descripcion_alcance": { "type": "string", "description": "Resumen ejecutivo del objeto del contrato y alcance general" }
      }
    },
    "cronograma": {
      "type": "object",
      "properties": {
        "fecha_publicacion": { "type": "string", "format": "date-time" },
        "fecha_limite_aclaraciones": { "type": "string", "format": "date-time" },
        "fecha_limite_modificaciones": { "type": "string", "format": "date-time" },
        "fecha_limite_presentacion": { "type": "string", "format": "date-time" },
        "fecha_apertura": { "type": "string", "format": "date-time" },
        "mejora_precio": {
          "type": "object",
          "properties": {
            "aplica": { "type": "boolean" },
            "condiciones": { "type": "string" }
          }
        }
      }
    },
    "esquema_participacion": {
      "type": "object",
      "properties": {
        "consorcio": {
          "type": "object",
          "properties": {
            "aplica": { "type": "boolean" },
            "condiciones": { "type": "string" }
          }
        },
        "representante_casas_extranjeras": { "type": "boolean" },
        "oferta_en_conjunto": { "type": "boolean" }
      }
    },
    "garantias": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tipo": { "type": "string", "example": "Participación / Cumplimiento" },
          "descripcion": { "type": "string" },
          "monto": { "type": "string" },
          "porcentaje": { "type": "number" },
          "vigencia": { "type": "string" }
        }
      }
    },
    "criterios_evaluacion_requisitos": {
      "type": "object",
      "properties": {
        "requisitos_admisibilidad": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Lista de condiciones obligatorias Pasa/No Pasa"
        },
        "slas_compromiso": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Niveles de servicio solicitados"
        },
        "criterios_puntuacion": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "criterio": { "type": "string" },
              "porcentaje_puntos": { "type": "string" }
            }
          }
        },
        "referencias_solicitadas": { "type": "string" },
        "cartas_fabricante": {
          "type": "object",
          "properties": {
            "requeridas": { "type": "boolean" },
            "detalle": { "type": "string" }
          }
        },
        "documentacion_espanol": {
          "type": "object",
          "properties": {
            "requerida": { "type": "boolean" },
            "tipo_traduccion": { "type": "string", "example": "Oficial / Simple / No aplica" }
          }
        },
        "multas_penales": { "type": "string" },
        "requisitos_legales": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "condiciones_ejecutivas": {
      "type": "object",
      "properties": {
        "vigencia_contrato": { "type": "string" },
        "prorroga_contrato": {
          "type": "object",
          "properties": {
            "aplica": { "type": "boolean" },
            "condiciones": { "type": "string" }
          }
        },
        "alcance_trabajo_detallado": { "type": "string" },
        "condiciones_pago": { "type": "string" }
      }
    }
  }
}
```

El agente debe devolver **únicamente** este JSON, sin texto adicional.

## Qué produce la app

Un archivo JSON válido (según el esquema anterior) con el análisis estructurado de la licitación pública, conteniendo:

- Identificación y clasificación del concurso
- Datos financieros y presupuesto (CRC → USD)
- Gestión y contacto (administrador de contrato)
- Alcance general
- Cronograma y fechas clave
- Esquema general de participación (consorcio, casas extranjeras, oferta en conjunto)
- Garantías (tipo, descripción, monto, porcentaje, vigencia)
- Criterios de evaluación, admisibilidad y aspectos legales
- Condiciones ejecutivas del contrato (vigencia, prórroga, alcance detallado, condiciones de pago)

Si un dato no está disponible en los insumos, su valor será `"No indica"` o `null`.

## Quién decide

- **El agente de IA** decide qué valor extraer de cada campo basándose en el contenido de los documentos de insumos.
- **La aplicación (código)** aplica las reglas de negocio: validación del JSON, cálculo de presupuesto USD, asignación de valores por defecto cuando faltan datos, y formato de salida.
- **El usuario humano** revisa y valida el JSON producido antes de usarlo en cualquier proceso oficial de contratación pública.

## Cifras de control

- Garantía mínima confirmada en el pliego: **36 meses** (contados a partir de la recepción definitiva de la solución).
- Tipo de cambio: se usa el **tipo de cambio de venta de referencia del BCCR** vigente a la fecha de apertura de ofertas.
- Redondeo del presupuesto en USD: **2 decimales**.
- Carta de fabricante: debe estar vigente y emitida dentro de los **3 meses anteriores** a la fecha de presentación de la oferta.

## Casos límite

1. **PDF escaneado sin texto**: Si `DETALLE CONCURSO.pdf` no tiene texto extraíble, los campos que probablemente contiene (número de licitación, tipo, presupuesto, fechas clave, mejora de precio, etc.) se devuelven como `"No indica"` o `null`. Se debe informar al usuario que se requiere una versión con OCR o texto legible.

2. **Campo ausente en ambos documentos**: Cualquier campo del esquema JSON que no aparezca explícitamente en el pliego Word ni en el PDF se devuelve como `"No indica"` (texto) o `null` (numérico/booleano). Nunca se inventa.

3. **Presupuesto sin monto en CRC**: Si no se encuentra un monto de presupuesto en CRC en los insumos, `presupuesto_crc` es `null`, y por tanto `presupuesto_usd` también es `null` (no se puede calcular la división).

4. **Tipo de cambio BCCR no disponible**: Si no se proporciona el tipo de cambio de venta del BCCR, `tipo_cambio_bccr` es `null` y `presupuesto_usd` es `null`.

5. **Garantía sin monto ni porcentaje**: El pliego confirma garantía de 36 meses pero no especifica monto ni porcentaje. En ese caso, `monto` y `porcentaje` se devuelven como `"No indica"` o `null`, y solo `vigencia` contiene "36 meses".

6. **Oferta en Conjunto vs. Consorcio**: El pliego menciona "Ofertas en Consorcio" pero no "Oferta en Conjunto" como campo separado. `oferta_en_conjunto` se devuelve como `false` o `null` hasta confirmar si aplica.

## Reglas del sistema

1. **No inventar datos**: Toda información debe estar fundamentada en los documentos aportados. Si un parámetro no está especificado explícitamente, se asigna `"No indica"` o `null`.

2. **Solo dos fuentes de entrada**: Pliego de Condiciones (Cartel) y Detalle del Concurso. No se consultan fuentes externas excepto para el tipo de cambio BCCR.

3. **Salida siempre JSON**: El agente responde siempre con la estructura JSON válida definida, sin texto decorativo ni bloques fuera de la estructura.

4. **No modificar insumos**: Los archivos dentro de la carpeta `insumos/` nunca se modifican.

5. **Contexto de referencia**: El archivo `contexto/Contexto_Mi_App.md` describe los campos a extraer y el esquema JSON. Es la guía de referencia del agente, pero no es una fuente de datos de la licitación.

6. **Idioma**: La aplicación opera en español, acorde al marco de contratación administrativa de Costa Rica.