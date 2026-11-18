# Decisiones técnicas — `docs/analisis-pqc.md`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

P2-1 a P2-5: inventario, estándares, planes, bytes/TLS y dos decisiones.

## Fuentes primarias

Los bytes PQC se atribuyen a FIPS 203/204/205; los formatos clásicos a RFC pertinentes y la muestra RSA a una medición local. No se atribuyen cifras de RSA a un estándar de ML-KEM.

## Separar objetivos

ML-KEM establece secretos; ML-DSA y SLH-DSA firman. HNDL amenaza confidencialidad, mientras que firmas y evidencia histórica requieren su propia estrategia.

## Corregir simplificaciones

Se distingue colisión de preimagen, λ de infidelidad, calendario histórico de vigente y grupo híbrido de autenticación PQC. La fidelidad al objetivo académico no exige repetir una afirmación técnicamente incorrecta del ejemplo.

## Planes verificables

Cada perfil identifica activos, sensibilidad, responsables, hitos y riesgos. Los meses relativos son propuestas de ejecución; no se presentan como fechas impuestas por NIST o por legislación colombiana.

## Rendimiento honesto

Se calcula el sobrecosto de bytes pero no se inventan tiempos de firma ni latencia de red. La selección ML-DSA se apoya en tamaños y caracterización cualitativa; un despliegue requiere benchmark del proveedor.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
