Necesito crear un analista de contratación publica, para revisar algunos puntos del pliego de licitaciones de la contratación administrativa, requiero que del pliego de licitación y del detalle del consurso extraiga la siguiente información 
Número de Licitación 
Tipo de Licitación 
Tipo de Concurso 
Presupuesto sale en colones, dividir por el tipo de cambio del BBCR ( banco central de costa rica ) y colocar como presupuesto 
Presupuesto en colonres  CRC
Presupuesto en dólares USD
Administrador de Contrato 
Descripción / Alcance
Fecha de Publicación 
Fecha de Apertura 
Fecha Límite Aclaraciones 
Fecha Límite Modificaciones
Fecha Límite Presentación 
Mejora de Precio si o no 
Esquema General 
Consorcio si aplica o no 
Representante Casa Extranjeras
Oferta en Conjunto
Descripción General de Garantía 
Monto de Garantía
Porcentaje de Garantía (%)
Vigencia de Garantía
Requisitos de Admisibilidad 
SLAs de Compromiso 
Requisitos de Puntuación / Evaluación 
Información de Referencias Solicitadas
Cartas de Fabricantes
Documentación del Fabricante en Español
Multas y/o Cláusulas Penales 
Requisitos Legales 
Vigencia del Contrato 
Prórroga del Contrato
Alcance del Trabajo
Condiciones de Pago
Toda esta información se encuentra en el pliego de condiciones y el detalle del concurso. 
¡Sí, el contexto está perfectamente claro! Entiendo con total exactitud lo que necesitas construir y estructurar.
Estás definiendo el perfil/prompt de un Analista Virtual de Contratación Pública (enfocado en el marco de contratación administrativa de Costa Rica, usando plataformas como SICOP y los tipos de cambio del BCCR). Tu objetivo es que la aplicación procese dos fuentes de entrada principales:
El Pliego de Condiciones (Cartel).
El Detalle del Concurso (datos generales de la plataforma/sistema).
Para asegurar que tu aplicación funcione sin vacíos, aquí tienes la estructura lógica completa organizada por bloques temáticos con los que el modelo o sistema debe extraer la información:
📋 Estructura de Extracción de Datos
1. Identificación y Clasificación del Concurso
Número de Licitación: (Ej. 2026LN-000001-XXXX)
Tipo de Licitación: (Licitación Mayor, Menor, Reducida, etc.)
Tipo de Concurso: (Nacional / Internacional)
2. Datos Financieros y Presupuesto
Presupuesto Estimado (CRC): (Monto original en colones)
Tipo de Cambio BCCR Aplicado: (Tipo de cambio de venta/referencia utilizado)
Presupuesto Estimado (USD): [Presupuesto CRC] ÷ [Tipo de Cambio BCCR]
3. Gestión y Contacto
Administrador del Contrato: (Nombre, unidad o departamento responsable)
4. Alcance y Descripción de la Contratación
Descripción / Alcance General: (Resumen ejecutivo del objeto contractual)
5. Cronograma y Fechas Clave
Fecha de Publicación:
Fecha Límite para Aclaraciones:
Fecha Límite para Modificaciones:
Fecha Límite de Presentación de Ofertas:
Fecha y Hora de Apertura de Ofertas:
Aplica Mejora de Precio: (Sí / No + condiciones si aplica)
6. Esquema General de Participación
Permite Consorcio: (Sí / No + condiciones)
Requiere Representante de Casas Extranjeras: (Sí / No)
Permite Oferta en Conjunto: (Sí / No)
7. Garantías (Participación / Cumplimiento)
Descripción General de la Garantía:
Monto de la Garantía: (En CRC y/o USD)
Porcentaje de la Garantía (%):
Vigencia requerida de la Garantía:
8. Criterios de Evaluación, Admisibilidad y Aspectos Legales
Requisitos de Admisibilidad: (Condiciones obligatorias "pasa/no pasa")
Requisitos de Puntuación / Evaluación: (Desglose de la tabla de evaluación y porcentajes)
SLAs de Compromiso: (Niveles de servicio requeridos)
Información de Referencias Solicitadas: (Cantidad de cartas, años de experiencia, contratos similares)
Cartas de Fabricantes: (¿Requeridas? Sí/No + especificaciones)
Documentación del Fabricante en Español: (¿Obligatoria traducción oficial o simple?)
Multas y/o Cláusulas Penales: (Porcentajes por día de atraso, topes máximos)
Requisitos Legales: (Personería, declaraciones juradas, al día con CCSS/FODESAF, etc.)
9. Condiciones Ejecutivas del Contrato
Vigencia del Contrato: (Plazo inicial)
Prórrogas del Contrato: (¿Aplica? Duración y condiciones)
Alcance Detallado del Trabajo:
Condiciones y Forma de Pago: (Plazos de pago, facturación, hitos)
🛠️ Recomendación Técnica para tu Aplicación
Para que tu aplicación funcione de manera óptima al procesar los documentos, te aconsejo configurar la lógica de extracción bajo estas tres reglas:
Regla de Extracción Nula (N/A): Si un dato no se encuentra de forma explícita en el pliego o detalle, el analista debe responder No indica / No aplica en lugar de inventar o asumir la información.
Conversión Dinámica de Moneda: Para el cálculo del presupuesto en USD, la aplicación debe solicitar o integrar la API/Web Scraping del Tipo de Cambio de Venta del BCCR para la fecha de la consulta.
Manejo de Formato: Puedes indicarle al backend/prompt que devuelva esta salida en formato JSON si lo vas a procesar en una base de datos o interfaz web, o en formato Markdown/Tabla si es para consumo directo de un usuario.
¿Te gustaría que te ayude a redactar el System Prompt exacto para el modelo de IA o la estructura JSON para la API de tu app?
Eres un Analista Experto en Contratación Pública y Contratación Administrativa en Costa Rica (plataforma SICOP). Tu función principal es procesar detallada y minuciosamente los documentos de licitación provistos por el usuario (Pliego de Condiciones / Cartel y el Detalle del Concurso) y extraer la información estructurada respetando estrictamente los datos oficiales.
### INSTRUCCIONES DE EXTRACCIÓN Y REGLAS DE NEGOCIO:
1. FUENTES DE INFORMACIÓN:
   - Extrae únicamente información fundamentada en los documentos aportados. No asumas ni inventes datos.
   - Si un parámetro o campo no está especificado explícitamente en el pliego o detalle, debes asignar el valor exacto: "No indica" o null en JSON.
2. CÁLCULO DE PRESUPUESTO Y MONEDA:
   - Identifica el Presupuesto Estimado en Colones Costa-ricenses (CRC).
   - Utiliza el Tipo de Cambio de Venta oficial del Banco Central de Costa Rica (BCCR) correspondiente a la fecha de la consulta o el provisto en el contexto.
   - Calcula el Presupuesto en USD realizando la división: [Presupuesto en CRC] ÷ [Tipo de Cambio BCCR]. Redondea el resultado a 2 decimales.
3. REVISIÓN CRÍTICA DE CRITERIOS:
   - Distingue claramente entre Requisitos de Admisibilidad ("Pasa / No Pasa", obligatorios) y Criterios de Evaluación / Puntuación (asignación de puntos/porcentajes).
   - En el apartado de Garantías, detalla explícitamente si se trata de Garantía de Participación o de Cumplimiento, su porcentaje, monto y vigencia.
   - En la sección de Fabricantes, verifica si se exigen cartas de respaldo y si se requiere traducción oficial o simple para la documentación técnica.
4. FORMATO DE SALIDA:
   - Responde SIEMPRE utilizando la estructura JSON válida definida para esta aplicación, sin agregar texto decorativo adicional ni bloques fuera de la estructura.
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