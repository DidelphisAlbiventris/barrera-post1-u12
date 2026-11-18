# Decisiones técnicas — `tests/test_circuitos.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

Comprobar propiedades cuánticas y límites del modelo.

## Pruebas independientes del muestreo

Statevector verifica probabilidades ideales y pureza. Así no se introduce una prueba frágil que falle porque Bell no produce exactamente 50/50 en 1024 mediciones.

## Casos asimétricos

Los cuatro objetivos incluyen 01 y 10, necesarios para detectar errores de orden de bits que no se ven en 00/11.

## Límites físicos

λ=0 debe recuperar el ideal y λ=1 debe producir distribución uniforme. Estos extremos comprueban que el ruido se aplica de verdad, no solo que se construyó un objeto NoiseModel.

## Validación de configuración

Para las tasas educativas se comprueba normalización y una probabilidad entre 0,95 y 1. Ese rango es una comprobación de regresión de este circuito pequeño, no una promesa para cualquier backend.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
