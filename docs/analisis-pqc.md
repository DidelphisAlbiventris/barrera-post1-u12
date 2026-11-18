# U12 — Impacto cuántico y migración postcuántica

**Estudiante:** Johan Barrera · **Código:** 1152538  
**Asignatura:** Arquitectura de computadores · **Fecha de revisión:** 16 de noviembre de 2026

## Alcance y criterio de evidencia

El análisis distingue resultados de simulación, tamaños normativos y propuestas de arquitectura. Los horizontes de 50–75, 5–7 y 25–50 años corresponden a los perfiles hipotéticos del enunciado; no se presentan como plazos legales de retención. Tampoco se presupone que una computadora cuántica criptográficamente relevante aparecerá en una fecha determinada. La amenaza se evalúa antes de su materialización porque una comunicación capturada hoy puede seguir siendo sensible cuando exista capacidad de descifrarla.

Los tamaños PQC se toman de FIPS 203, 204 y 205. No se confunden los nombres de las propuestas Kyber/Dilithium/SPHINCS+ con cualquier implementación final compatible con ML-KEM/ML-DSA/SLH-DSA. Las recomendaciones de migración son propuestas del análisis, sujetas a pruebas y al marco aplicable a cada organización.

## 1. Inventario y vulnerabilidad — checkpoint P2-1

| Algoritmo | Uso | Amenaza cuántica | Consecuencia | Remediación propuesta |
|---|---|---|---|---|
| RSA-2048 / RSA-3072 | Firma y establecimiento de secretos según protocolo | Shor: factorización | Recuperación de claves; falsificación o descifrado según el uso | ML-DSA para firmas; ML-KEM para establecimiento, con transición de protocolo |
| ECDSA P-256 | Firma | Shor: logaritmo discreto elíptico | Falsificación futura | Migración de firmantes, verificadores y PKI hacia firmas PQC |
| ECDH X25519 | Acuerdo de clave | Shor: logaritmo discreto | Recuperación del secreto de sesiones registradas | X25519MLKEM768 durante transición, cuando el protocolo lo soporte |
| DH-2048 | Acuerdo de clave | Shor: logaritmo discreto | Compromiso del secreto compartido | Establecimiento PQC o híbrido aprobado para el protocolo |
| AES-128 | Cifrado simétrico | Grover: búsqueda genérica ideal de orden 2^64 consultas | Reducción teórica del costo de búsqueda; no ruptura práctica demostrada | Valorar AES-256 para nuevos sistemas de larga sensibilidad |
| AES-256 | Cifrado simétrico | Grover: orden 2^128 consultas ideales | Margen elevado; no equivalente a RSA roto | Mantener claves, nonces y modo autenticado correctamente gestionados |
| SHA-256 | Hash | Preimagen: Grover, orden 2^128; colisiones: otro problema | Depende de la propiedad de seguridad requerida | Evaluar SHA-384/512 donde se necesite mayor margen, sin declarar SHA-256 universalmente roto |
| SHA3-256 | Hash | Mismas cotas genéricas de preimagen para salida de 256 bits | La familia no evita la aceleración genérica | Dimensionar longitud según aplicación y política |

Shor compromete la premisa matemática de RSA y ECC ante una computadora cuántica suficientemente grande y tolerante a fallos. Aumentar moderadamente el tamaño de RSA no corrige esa vulnerabilidad. En cambio, las cifras de Grover son complejidades ideales de consultas, no tiempos de ejecución ni presupuestos de ataque. La profundidad, el costo del oráculo, la corrección de errores y las limitaciones de paralelización importan (NIST, s. f.; Banerjee et al., 2026).

Se separa **preimagen** de **colisión**. Buscar un mensaje para un hash fijado no equivale a encontrar cualquier pareja con el mismo hash. La cota cuántica genérica de colisiones de orden 2^(n/3), bajo supuestos de acceso y memoria, corresponde a algoritmos de colisión como el de Brassard–Høyer–Tapp, no a aplicar directamente Grover a una búsqueda de preimagen. Por tanto, no se atribuyen los aproximadamente 85 bits de consultas para colisiones de una salida de 256 bits a Grover.

La amenaza **HNDL** consiste en capturar tráfico cifrado para intentar descifrarlo después. Incluso una sesión con secreto hacia adelante basado en ECDHE puede quedar expuesta a Shor si se registraron los intercambios públicos necesarios. La autenticación de documentos plantea otra amenaza: falsificar firmas o perder capacidad de validar evidencia histórica. Ambos problemas requieren migraciones, pero no son el mismo objetivo de seguridad.

## 2. Estándares NIST de 2024 — checkpoint P2-2

### ML-KEM: establecimiento de secretos, no firma

ML-KEM se basa en retículos modulares y la dificultad de Module Learning with Errors. Produce un secreto que puede alimentar cifrado simétrico autenticado; no firma prescripciones ni cifra directamente archivos arbitrarios. FIPS 203, tablas 2–3, proporciona:

| Parámetro | Categoría NIST | Pública (B) | Privada expandida (B) | Ciphertext (B) | Secreto (B) |
|---|---:|---:|---:|---:|---:|
| ML-KEM-512 | 1 | 800 | 1632 | 768 | 32 |
| ML-KEM-768 | 3 | 1184 | 2400 | 1088 | 32 |
| ML-KEM-1024 | 5 | 1568 | 3168 | 1568 | 32 |

Las categorías 1, 3 y 5 usan referencias de costo asociadas a AES-128, AES-192 y AES-256; no significan automáticamente 128, 192 o 256 bits de seguridad cuántica en cualquier modelo. Se propone 768 como equilibrio para A/B y el parámetro exigido por la política específica para C.

### ML-DSA: firmas de uso general

ML-DSA es una firma sobre retículos modulares; su análisis involucra MLWE y problemas de vectores cortos modulares, además del modelo de hash. Reducir toda su seguridad a una sola frase sobre MLWE resulta incompleto. FIPS 204, tabla 2, especifica:

| Parámetro | Categoría NIST | Pública (B) | Privada expandida (B) | Firma (B) |
|---|---:|---:|---:|---:|
| ML-DSA-44 | 2 | 1312 | 2560 | 2420 |
| ML-DSA-65 | 3 | 1952 | 4032 | 3309 |
| ML-DSA-87 | 5 | 2592 | 4896 | 4627 |

Aumentar el parámetro amplía estructuras y tráfico. La verificación debe medirse con la biblioteca y CPU seleccionadas: un estándar de formato no garantiza milisegundos por operación. ECDSA P-256 tiene firmas mucho menores, pero no resistencia postcuántica; no es una alternativa de seguridad equivalente.

### SLH-DSA: diversidad de supuestos

SLH-DSA usa firmas hash sin estado persistente de índice. Evita depender de retículos, a costa de firmas grandes y más trabajo de hash. Su seguridad no depende *únicamente* de colisiones: intervienen propiedades de preimagen, funciones seudoaleatorias y componentes de la construcción. FIPS 205, tabla 2 y estructura de claves, fija:

| Variante SHA2 o SHAKE | Categoría | Pública (B) | Privada (B) | Firma (B) |
|---|---:|---:|---:|---:|
| 128s | 1 | 32 | 64 | 7856 |
| 128f | 1 | 32 | 64 | 17088 |
| 192s | 3 | 48 | 96 | 16224 |
| 192f | 3 | 48 | 96 | 35664 |
| 256s | 5 | 64 | 128 | 29792 |
| 256f | 5 | 64 | 128 | 49856 |

`s` prioriza firmas pequeñas; `f`, generación rápida. Las variantes SHA2 y SHAKE correspondientes comparten esos tamaños.

### Velocidad relativa y función correcta

| Familia | Operación y uso | Velocidad relativa cualitativa | Fuente y límite |
|---|---|---|---|
| ML-KEM | Encapsular/desencapsular para establecer claves | Operación de KEM; no comparable directamente con firmar | FIPS 203 define operaciones, no una latencia universal |
| ML-DSA | Firmar/verificar documentos | Generalmente más rápida que SLH-DSA para firma/verificación | RFC 9958 §10.2; depende de implementación y plataforma |
| SLH-DSA | Firmar con diversidad basada en hash | Generalmente más lenta; `f` acelera firma frente a `s` a costa de tamaño | FIPS 205 §11 y RFC 9958 §10.2 |
| ECDSA P-256 | Firma clásica | Referencia que se debe medir en el mismo equipo | No se inventa una razón de velocidades frente a ML-DSA |

No se han realizado benchmarks de criptografía PQC ni handshakes de red en este laboratorio. La comparación de velocidad es cualitativa y documentada; los bytes sí son cuantificables. Antes de producción se medirían firma/s, verificación/s, uso de CPU/memoria y percentiles de latencia bajo carga.

## 3. Plan de migración — checkpoint P2-3

Se propone un inventario con campos: activo, propietario, protocolo, algoritmo/parámetro, biblioteca y versión, proveedor/HSM, ubicación de certificados, vida útil del dato, dependencia externa, posibilidad de actualización y evidencia de prueba. El inicio **M0** es la aprobación del proyecto; los plazos M+ son propuestas, no mandatos del NIST. La priorización combina duración de la sensibilidad, exposición y tiempo necesario para reemplazar sistemas.

### Perfil A: hospital universitario

**Inventario y datos:** portal de pacientes y APIs TLS, VPN con sedes, intercambio con laboratorios, PKI de prescriptores, HSM, copias de historias clínicas y claves que envuelven claves de datos. El horizonte de 50–75 años y la exposición de los registros hacen prioritaria la confidencialidad frente a HNDL. Cifrar discos con AES-256 no elimina una envoltura RSA vulnerable ni el riesgo de transporte clásico.

**Estrategia:** TLS híbrido X25519MLKEM768 para clientes compatibles; ML-DSA-65 para nuevas prescripciones en un formato que también puedan validar los receptores; PKI paralela durante coexistencia. Se mantendría AES-256 autenticado para datos y se revisaría el mecanismo de distribución de claves. Una firma clásica de transición no debe anular la validación PQC requerida ni habilitar una degradación silenciosa.

| Fase propuesta | Responsable | Hito verificable |
|---|---|---|
| M0–M+2 | Seguridad + TI clínica | Inventario firmado por propietarios, clasificación y dependencias completas de sistemas críticos |
| M+3–M+5 | Redes + integración | Piloto TLS híbrido con clientes de prueba; registro de negociación, fallos y latencia p95 |
| M+6–M+9 | PKI + farmacia | Piloto ML-DSA-65: verificación cruzada, revocación, sello de tiempo y restauración de claves probados |
| M+10–M+12 | Operación + auditoría | Despliegue gradual de sistemas prioritarios, excepciones documentadas y ejercicio de recuperación |

**Riesgos y mitigaciones:** equipos médicos sin actualización → segmentación y pasarelas aprobadas; receptores que no verifican PQC → interoperabilidad previa y coexistencia explícita; pérdida de claves → respaldo HSM y simulacro; evidencia histórica → conservar cadena, estado de revocación y sellos, renovando evidencia antes de obsolescencia. El documento no presupone que una prescripción deja de necesitar autenticidad al terminar su uso clínico.

### Perfil B: comercio electrónico

**Inventario y datos:** CDN/balanceadores TLS 1.3, API móvil, webhooks de pagos, autenticación entre servicios, firma de despliegues, secretos en KMS y dependencias de la pasarela. El horizonte de 5–7 años es el supuesto del caso, no una autorización para almacenar datos de tarjeta innecesarios. Se mantendría minimización y tokenización conforme al entorno de pagos.

**Estrategia:** conservar AES-256 y activar el grupo híbrido en infraestructura compatible, evaluando negociación real. La autenticación ECDSA del servidor requiere un plan separado: cambiar el grupo KEX no convierte el certificado en postcuántico. La transición se planearía con el proveedor; no se afirmaría que PCI-DSS impone por sí mismo una fecha universal para PQC.

| Fase propuesta | Responsable | Hito verificable |
|---|---|---|
| M0–M+1 | Plataforma + seguridad | Lista de terminadores TLS, bibliotecas, clientes y contratos con proveedor |
| M+2–M+3 | Plataforma | Canary de híbrido; medir conexiones negociadas, fallos, bytes y p50/p95 por tipo de red |
| M+4–M+6 | Operación | Aumentar cobertura solo si cumple SLO acordado y compatibilidad; rollback ensayado |
| Cada 12 meses | Arquitectura | Revisión de estándares, clientes y criptoanálisis para decidir si procede PQC puro |

**Riesgos y mitigaciones:** middleboxes → pruebas de rutas y tamaños; clientes antiguos → compatibilidad registrada sin afirmar que reciben protección PQC; aumento de CPU/latencia → pruebas de carga y capacidad; dependencia del CDN → cláusulas de actualización y visibilidad de negociación. El retiro clásico requiere criterio verificable, no una fecha tomada de una política de defensa extranjera.

### Perfil C: defensa

**Inventario y datos:** VPN interagencias, PKI, firma de documentos, HSM, equipos de comunicaciones, firmware firmado y archivo clasificado. La sensibilidad de 25–50 años y el costo de reemplazo justifican prioridad alta. Se identificarían sistemas de larga vida y enlaces que atraviesan proveedores externos.

**Alcance normativo:** CNSA 2.0 se refiere a NSS estadounidenses y contextos expresamente comprendidos; no impone automáticamente obligaciones a toda entidad gubernamental colombiana. Para el perfil académico se adopta como referencia condicionada a que esa política resulte aplicable. La FAQ NSA de octubre de 2026, versión 2.2, actualiza el calendario: adquisiciones nuevas desde 1/1/2027; retirar equipos/servicios incapaces antes de finalizar 2030; uso exigido para completar la transición al finalizar 2031, con excepciones previstas. Por ello, el intervalo 2025–2033 del enunciado se identifica como referencia histórica, no como calendario vigente universal.

| Fase propuesta | Responsable | Hito verificable |
|---|---|---|
| 2026–inicio 2027 | Autoridad de seguridad + compras | Inventario y pliegos que exijan parámetros/perfiles aplicables; plan para componentes no actualizables |
| 2027–2028 | Redes + PKI | VPN y PKI piloto con productos aprobados; interoperabilidad y recuperación probadas |
| 2029–2030 | Operación + compras | Sustitución de componentes incompatibles; trazabilidad de cada excepción |
| 2031 | Autoridad acreditadora | Validación de cobertura y uso exigido de mecanismos resistentes según política aplicable |

**Estrategia:** cuando CNSA corresponda, ML-KEM-1024 y ML-DSA-87, con AES-256 y hashes autorizados; no sustituirlos arbitrariamente por parámetros de A/B. La coexistencia puede usar PKI paralela. Un mecanismo híbrido solo se adoptaría si está admitido por el perfil del protocolo; “clásico + PQC” por sí solo no prueba conformidad CNSA. En VPN se seguiría el perfil aprobado en lugar de inventar un combinador.

**Riesgos y mitigaciones:** equipos heredados → reemplazo presupuestado; exposición de secretos → dispositivos y procedimientos acreditados; fragmentación de mensajes → ensayos interoperables del protocolo; dependencia de proveedores → hitos contractuales y pruebas de aceptación. Si el organismo no está bajo CNSA, sus autoridades fijarían las obligaciones locales sin trasladar mecánicamente este calendario.

## 4. Tamaños y efecto en TLS — checkpoint P2-4

Todos los valores son bytes; se especifica la representación. Los FIPS son fuente de PQC, no de RSA, ECDSA ni X25519. Para estos últimos se usan RFC 8017, RFC 5480 y RFC 7748. La muestra RSA está registrada en `resultados/rsa_tamanos.json`, obtenida mediante `scripts/medir_rsa.py`; el script destruye la clave temporal.

| Algoritmo | Tipo | Pública | Privada | Firma / ciphertext | Seguridad y fuente |
|---|---|---:|---:|---:|---|
| RSA-3072 | Firma clásica | 422, muestra SPKI DER | 1767, muestra PKCS#1 DER | 384 firma | ~128 bits clásicos; RFC 8017, medición de muestra |
| ECDSA P-256 | Firma clásica | 65 SEC1 sin compresión (64 coordenadas + prefijo) | 32 escalar | 64 cruda; DER variable, comúnmente 70–72 | ~128 bits clásicos; RFC 5480; no PQC |
| X25519 | Acuerdo clásico | 32 | 32 | No firma; contribución pública 32 | ~128 bits clásicos; RFC 7748 |
| ML-KEM-768 | KEM PQC | 1184 | 2400 | 1088 ciphertext | Categoría 3; FIPS 203 tabla 3 |
| ML-DSA-65 | Firma PQC | 1952 | 4032 | 3309 firma | Categoría 3; FIPS 204 tabla 2 |
| SLH-DSA-SHA2-128s | Firma PQC | 32 | 64 | 7856 firma | Categoría 1; FIPS 205 tabla 2 |

El tamaño DER de RSA depende del contenido y del contenedor; 1767 no es una constante del algoritmo. La clave privada no se transmite en el handshake. Los tamaños PQC de esta tabla son los formatos expandidos del estándar, sin ASN.1 ni certificados.

Cálculos reproducibles:

- Clave pública ML-KEM-768 / X25519 = 1184 / 32 = **37 veces**.
- Firma ML-DSA-65 / ECDSA de 72 B = 3309 / 72 = **45,96 veces**. Con firma cruda de 64 B sería **51,70 veces**; no se mezclan representaciones.
- Contribución cliente X25519MLKEM768: 1184 + 32 = **1216 B**, frente a 32 B; aumento **1184 B**.
- Contribución servidor: 1088 + 32 = **1120 B**, frente a 32 B; aumento **1088 B**.
- Aumento conjunto de ambos contenidos: **2272 B**, sin contar cabeceras, otras extensiones o certificados.

Son longitudes del contenido `key_exchange` de la entrada `key_share`, no de toda la extensión ni de todo ClientHello. El protocolo y su orden de concatenación se implementan según **RFC 10024 (agosto de 2026)**. Los experimentos anteriores llamados X25519Kyber768Draft00 no son un nombre intercambiable para toda implementación de ML-KEM final.

El aumento de bytes puede ocupar más segmentos sin añadir una nueva ronda lógica a TLS 1.3. Si los datos caben en la ventana inicial disponible y no hay pérdidas, la segmentación no obliga por sí sola a un RTT adicional. Una cadena de certificados con firmas PQC añade varios kilobytes, según número de certificados, claves y codificación. Congestión, pérdidas, MTU, límites de middleboxes, ventanas y negociación mediante HelloRetryRequest pueden alterar la latencia. No se promete un sobrecosto de cero milisegundos ni que siempre cabe en un paquete. Se propone medir p50/p95 y retransmisiones en redes reales antes de aceptar el cambio.

## 5. Decisión técnica: firma de prescripciones — checkpoint P2-5

Se recomienda **ML-DSA-65** como firma principal del perfil hospitalario, una vez validada su integración con el formato de prescripción, el HSM y los receptores. ML-KEM se descarta para esta función porque encapsular una clave compartida no autentica mediante una firma el contenido y emisor de una prescripción. Entre las alternativas exigidas por el caso, ML-DSA-65 genera firmas de 3309 bytes frente a 7856 de SLH-DSA-128s, por lo que reduce tráfico y almacenamiento; la caracterización de rendimiento de RFC 9958 también favorece ML-DSA para un flujo frecuente de firma y verificación. No obstante, se debe medir la implementación concreta: no se deduce una latencia exacta solamente del nombre del algoritmo. Además, las categorías difieren —3 frente a 1—; una comparación al mismo nivel incluiría SLH-DSA-192s, de 16224 bytes.

El horizonte de confidencialidad de historias clínicas no obliga automáticamente a usar SLH-DSA para cada prescripción. HNDL concierne al descifrado posterior; la autenticidad exige prevenir falsificaciones y preservar evidencia de emisión. Una prescripción sí puede necesitar verificación histórica, de modo que se contemplan sellos de tiempo, archivo de certificados y revocación, y renovación de evidencia antes de obsolescencia. SLH-DSA se reserva como alternativa de diversidad criptográfica o para roles de baja frecuencia y larga vida donde su costo sea aceptable, por ejemplo una raíz de confianza si el ecosistema lo admite. No se justifica con la afirmación incorrecta de que su seguridad depende exclusivamente de resistencia a colisiones.

## 6. Decisión técnica: híbrido en comercio electrónico — checkpoint P2-5

Se recomienda adoptar **TLS híbrido como estrategia de transición**, empezando por un piloto medido. El incremento calculado de 2272 bytes en los dos intercambios de clave es manejable en muchas conexiones, pero no constituye por sí mismo una medición de latencia. La decisión debe comprobarse contra los SLO y las redes de los clientes. La ventaja es conservar una capa tradicional bien estudiada mientras se incorpora protección frente a Shor: un combinador y protocolo correctos buscan mantener seguro el secreto aunque falle uno de sus componentes. Esta protección no exige suponer independencia estadística perfecta entre todas las posibles fallas, ni evita errores comunes de implementación. Asimismo, un intercambio X25519+ML-KEM no protege automáticamente una firma ECDSA ni convierte la autenticación del servidor en una firma híbrida.

No se propone mantener la complejidad indefinidamente por inercia. Se plantea revisar anualmente la madurez de ML-KEM, los estándares para PQC puro, la compatibilidad de clientes, la seguridad de bibliotecas y el costo operativo. El componente clásico podrá retirarse cuando existan soporte, política y pruebas suficientes, preservando posibilidad de recuperación. El horizonte de 5–7 años permite una priorización distinta a salud, pero no elimina el riesgo de datos ya capturados. Los plazos de CNSA sirven como contexto de otro sector y no obligan a esta startup ni fijan automáticamente su retiro híbrido en 2033. Tampoco se interpreta “transición” como un compromiso de retirarlo antes de que sea técnicamente conveniente.

## Referencias en formato APA

National Institute of Standards and Technology. (2024a). *Module-lattice-based key-encapsulation mechanism standard* (FIPS 203). https://doi.org/10.6028/NIST.FIPS.203

National Institute of Standards and Technology. (2024b). *Module-lattice-based digital signature standard* (FIPS 204). https://doi.org/10.6028/NIST.FIPS.204

National Institute of Standards and Technology. (2024c). *Stateless hash-based digital signature standard* (FIPS 205). https://doi.org/10.6028/NIST.FIPS.205

National Institute of Standards and Technology. (s. f.). *Post-quantum cryptography: FAQs*. Consultado el 16 de noviembre de 2026. https://csrc.nist.gov/projects/post-quantum-cryptography/faqs

Banerjee, A., Reddy, T., Schoinianakis, D., Hollebeek, T., & Ounsworth, M. (2026). *Post-quantum cryptography for engineers* (RFC 9958). https://www.rfc-editor.org/rfc/rfc9958.html

Kwiatkowski, K., Kampanakis, P., Westerbaan, B. E., & Stebila, D. (2026). *Post-quantum traditional (PQ/T) hybrid key agreement mechanisms for TLS 1.3* (RFC 10024). https://www.rfc-editor.org/rfc/rfc10024.html

National Security Agency. (2026, octubre). *Commercial National Security Algorithm Suite 2.0 and quantum computing: Frequently asked questions* (versión 2.2). https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/1/CSI_CNSA_2.0_FAQ_.PDF

National Security Agency. (s. f.). *CNSA Suite*. Consultado el 16 de noviembre de 2026. https://www.nsa.gov/Resources/CNSA-Suite/

Moriarty, K., Kaliski, B., & Rusch, A. (2016). *PKCS #1: RSA cryptography specifications version 2.2* (RFC 8017). https://www.rfc-editor.org/rfc/rfc8017.html

Turner, S., Brown, D., Yiu, K., Housley, R., & Polk, T. (2009). *Elliptic curve cryptography subject public key information* (RFC 5480). https://www.rfc-editor.org/rfc/rfc5480.html

Langley, A., Hamburg, M., & Turner, S. (2016). *Elliptic curves for security* (RFC 7748). https://www.rfc-editor.org/rfc/rfc7748.html

Brassard, G., Høyer, P., & Tapp, A. (1997). *Quantum algorithm for the collision problem*. https://arxiv.org/abs/quant-ph/9705002
