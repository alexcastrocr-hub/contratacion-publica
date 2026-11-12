# PLAN.md

## 1. RESUMEN

Vamos a construir una aplicación web tipo Analista Virtual de Contratación Pública para Costa Rica (SICOP, BCCR). Entra como insumo el Pliego de Condiciones (Word) y el Detalle del Concurso (PDF, posiblemente escaneado). El agente de IA extrae información estructurada de ambos documentos y la devuelve en un contrato JSON válido. Sale como resultado una pantalla web con contadores, tablas con filtro y descarga del JSON, todo validado contra cifras de control y casos límite definidos en AGENTS.md.

## 2. LO QUE ENCONTRÉ

**Carpeta `contexto/`:**
- `Contexto_Mi_App.md` (246 líneas): define 32 campos a extraer en 9 bloques, reglas de negocio (no inventar, tipo de cambio BCCR, admisibilidad vs evaluación, salida siempre JSON) y el esquema JSON completo del contrato de salida.
- `Número de Licitación (1).docx`: documento fuente del contexto (no se modificará).

**Carpeta `insumos/`:**
- `PLIEGO DE CONDICIONES ALMACENAMIENTO NAS MODIFICADO.docx`: Word legible, 1032 párrafos, 14 tablas. Contiene objeto contractual (NAS empresarial para BCCR), garantía 36 meses, tipo de cambio BCCR, consorcio, requisitos de admisibilidad, SLAs, estructura de precio, requisitos legales, multas, alcance del trabajo, condiciones de pago, administrador de contrato.
- `DETALLE CONCURSO.pdf`: 4 páginas, **PDF escaneado**, 0 caracteres de texto extraíble. No se pudo leer su contenido.

**Coincidencia con AGENTS.md:**
AGENTS.md ya documenta lo encontrado. Sin embargo, hay campos del contexto que no aparecen confirmados en el pliego Word ni en el PDF escaneado: Número de Licitación, Tipo de Licitación, Tipo de Concurso, Presupuesto Estimado (monto CRC/USD), Fechas clave (Publicación, Apertura, Límite Aclaraciones, Límite Modificaciones, Límite Presentación), Mejora de Precio, Esquema General, Representante Casa Extranjeras, Oferta en Conjunto, Monto de Garantía, Porcentaje de Garantía (%), Requisitos de Puntuación/Evaluación, Referencias Solicitadas, Documentación del Fabricante en Español, Condiciones de Pago específicas. Es probable que estén en el PDF escaneado, pero no se puede confirmar sin OCR.

## 3. ENTREGAS POR SUBAGENTE

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 1 | @backend | Estructura base MVC con `uv`: `app/__init__.py` con `create_app()`, `app/controllers/`, `app/services/`, `wsgi.py`, `.env` (sin llaves reales), `iniciar_app.bat`. Instalación de Flask y python-dotenv con `uv add`. | `app/__init__.py`, `app/controllers/`, `app/services/`, `wsgi.py`, `.env.example`, `iniciar_app.bat`, `pyproject.toml`/`uv.lock` | Ninguno (entrega inicial). | Ejecutar `iniciar_app.bat` y ver que abre el navegador en `http://localhost:5000` sin errores de importación. |
| 2 | @backend | Lectura del pliego Word con `python-docx`: servicio que extrae texto y tablas de `PLIEGO DE CONDICIONES ALMACENAMIENTO NAS MODIFICADO.docx` y devuelve un diccionario Python. | `app/services/lectura_pliego.py` | Entrega 1 (estructura MVC funcionando). | Ejecutar `uv run python -c "from app.services.lectura_pliego import extraer_pliego; print(extraer_pliego()['texto'][:200])"` y ver texto del pliego en consola. |
| 3 | @backend | Regla R1 - Valor por defecto para datos ausentes: función `valor_por_defecto(campo)` que devuelve `"No indica"` o `null` si el campo no está en los insumos. | `app/services/regla_valor_por_defecto.py` | Entrega 2 (servicio de lectura funcionando). | Llamar a la función con un campo inexistente y ver que devuelve `"No indica"` o `null`. |
| 4 | @backend | Regla R2 - Cálculo presupuesto USD: función `calcular_presupuesto_usd(presupuesto_crc, tipo_cambio_bccr)` que divide y redondea a 2 decimales. | `app/services/regla_presupuesto_usd.py` | Entrega 3 (regla R1 funcionando). | Llamar con `presupuesto_crc=1000000` y `tipo_cambio_bccr=500` y ver `2000.0` en pantalla/consola. |
| 5 | @backend | Regla R3 - Distinguir admisibilidad vs evaluación: funciones `extraer_requisitos_admisibilidad()` y `extraer_criterios_puntuacion()` que separan correctamente ambos tipos. | `app/services/regla_admisibilidad_evaluacion.py` | Entrega 4 (regla R2 funcionando). | Llamar a ambas funciones con texto del pliego y ver listas separadas sin mezclar criterios. |
| 6 | @backend | Regla R4 - Garantías: función `extraer_garantias()` que identifica tipo, descripción, monto, porcentaje y vigencia (36 meses confirmados en pliego). | `app/services/regla_garantias.py` | Entrega 5 (regla R3 funcionando). | Llamar a la función y ver que la vigencia es `"36 meses"` y monto/porcentaje son `"No indica"` o `null`. |
| 7 | @backend | Regla R5 - Fabricantes: función `extraer_fabricantes()` que verifica si se requieren cartas de fabricante y tipo de traducción (oficial/simple). | `app/services/regla_fabricantes.py` | Entrega 6 (regla R4 funcionando). | Llamar a la función y ver `requeridas: true` y `tipo_traduccion` con el valor del pliego o `"No indica"`. |
| 8 | @backend | Integración del agente de IA: servicio que lee la llave de `.env`, envía los insumos al agente y devuelve el JSON según el contrato de AGENTS.md. | `app/services/agente_ia.py`, `.env` (llave real proporcionada por el usuario) | Entrega 7 (todas las reglas de negocio funcionando). | Ejecutar el servicio con una llave de prueba y ver que devuelve JSON válido sin texto decorativo. |
| 9 | @backend | Endpoint de descarga de resultados: controller que sirve el JSON generado para descarga desde el navegador. | `app/controllers/resultados.py` | Entrega 8 (integración IA funcionando). | Abrir `http://localhost:5000/resultados` y ver que se descarga o muestra el JSON. |
| 10 | @frontend | Pantalla de inicio (`inicio`): formulario en español para subir/seleccionar insumos y botón para iniciar análisis. | `app/templates/inicio.html`, ajuste en `app/templates/base.html` | Entrega 9 (endpoint de resultados funcionando). | Abrir `http://localhost:5000/inicio` y ver el formulario en español con botón de análisis. |
| 11 | @frontend | Pantalla de resultados (`resultados`): tablero con contadores grandes y tabla con filtro en español, mostrando el JSON del agente. | `app/templates/resultados.html`, CSS en `base.html` | Entrega 10 (pantalla de inicio funcionando). | Abrir `http://localhost:5000/resultados` y ver contadores, tabla con datos y filtro funcionando. |
| 12 | @frontend | Detalle por registro y estilo final de la app: vista de detalle de cada campo extraído, diseño profesional en español, sin librerías JS externas. | `app/templates/detalle.html`, ajustes CSS en `base.html` | Entrega 11 (pantalla de resultados funcionando). | Hacer clic en una fila de la tabla y ver el detalle de ese registro en pantalla. |
| 13 | @tester | Pruebas en `tests/` con pytest contra cifras de control y casos límite de AGENTS.md. | `tests/test_presupuesto.py`, `tests/test_garantias.py`, `tests/test_valor_por_defecto.py`, `tests/test_agente_ia.py` | Entrega 12 (app completa funcionando). | Ejecutar `uv run pytest` y ver todas las pruebas pasadas. |
| 14 | @tester | `VALIDACION.md`: reporte de esperado vs obtenido para cada caso límite y cifra de control. | `VALIDACION.md` | Entrega 13 (pruebas escritas y ejecutadas). | Abrir `VALIDACION.md` y verificar que cada fila tenga esperado, obtenido y estado (OK/DIFERENCIA). |
| 15 | @revisor | Revisión de seguridad: llaves expuestas, `.gitignore`, datos sensibles en código, revisión de que todo esté en AGENTS.md. | Ningún archivo (solo reporte de hallazgos) | Entrega 14 (VALIDACION.md entregado). | Revisor entrega lista de hallazgos con prioridad y corrección propuesta; se verifica que no haya secretos en el código. |

## 4. PUNTOS DE CONTROL

| Después de la entrega | Interviene @tester | Qué debe ver el usuario en pantalla |
|----------------------|--------------------|-------------------------------------|
| Entrega 1 (estructura MVC) | No | Navegador abre `http://localhost:5000` sin errores. |
| Entrega 4 (regla R2 presupuesto USD) | Sí | Al ejecutar la función con `1000000 / 500`, ver `2000.0` (2 decimales). |
| Entrega 6 (regla R4 garantías) | Sí | Ver vigencia `"36 meses"` y monto/porcentaje como `"No indica"` o `null`. |
| Entrega 9 (endpoint descarga) | Sí | Abrir `/resultados` y ver JSON descargable o visible en pantalla. |
| Entrega 11 (pantalla resultados) | Sí | Ver contadores grandes y tabla con filtro funcionando en español. |
| Entrega 13 (pruebas pytest) | Sí | Ejecutar `uv run pytest` y ver `X passed, 0 failed`. |
| Entrega 15 (revisor) | Sí | Revisor entrega lista de hallazgos; usuario confirma que no hay secretos en el código. |

## 5. RIESGOS

| Riesgo | Qué hará @backend | Qué hará @frontend | Qué hará @tester | Qué hará @revisor |
|--------|-------------------|--------------------|------------------|-------------------|
| Datos incompletos (campos faltantes en insumos) | Devolver `"No indica"` o `null` sin inventar, y registrar en log qué falta. | Mostrar claramente en pantalla qué campos son `"No indica"`. | Escribir prueba que verifique que campos ausentes devuelven `"No indica"`. | Verificar que no haya campos inventados fuera de AGENTS.md. |
| Archivo `DETALLE CONCURSO.pdf` escaneado sin texto | No intentar leer el PDF con pypdf (da 0 caracteres). Marcar como pendiente de OCR. | Mostrar aviso en pantalla: "El PDF está escaneado, algunos campos pueden no estar disponibles". | Incluir en VALIDACION.md que el PDF no tuvo texto extraíble. | Verificar que el aviso de PDF escaneado esté visible al usuario. |
| Respuesta del agente de IA que no es JSON válido | Validar la respuesta con `json.loads()`; si falla, devolver error controlado y `"No indica"` en los campos afectados. | Mostrar mensaje de error amigable en pantalla si el JSON no es válido. | Escribir prueba que inyecte respuesta no-JSON y verifique manejo de error. | Verificar que no se expongan claves de API en mensajes de error. |
| Límite de la llave gratis del agente de IA | Leer llave solo de `.env`; si falla por límite, devolver error y usar reglas de negocio locales como fallback. | Mostrar aviso si el servicio IA no está disponible. | Probar con llave inválida y verificar que la app no se rompe. | Verificar que la llave no esté hardcodeada en ningún archivo. |

## 6. PREGUNTAS PARA MÍ

Antes de empezar la construcción, necesito que confirme:

1. **¿Tiene ya una llave de API para el agente de IA?** Si no, ¿desea que el plan asuma un modo offline/fallback donde las reglas de negocio se apliquen localmente sin llamar a IA externa?
2. **¿Desea que intente hacer OCR del PDF escaneado (`DETALLE CONCURSO.pdf`) antes de construir, o acepta que los campos que probablemente están ahí se marquen como `"No indica"` por ahora?**
3. **¿Qué puerto prefiere para la aplicación?** El plan asume `5000`, pero puedo cambiarlo.
4. **¿Desea que agregue una entrega extra para configurar `.gitignore` y evitar que `.env` y `__pycache__` suban a GitHub?** (El revisor lo verificaría, pero podría ser parte de la entrega 1 del backend).

Quedo a la espera de su aprobación del PLAN.md y respuestas a estas preguntas antes de que cualquier subagente comience a construir.