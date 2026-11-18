# Decisiones técnicas — `src/bell_state.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

P1-1: preparar Bell, 1024 shots y figura con dos estados.

## H y CX

Se usan exactamente H(q0) y CX(q0,q1). La secuencia prepara la superposición coherente requerida con dos puertas. Usar dos H independientes generaría cuatro resultados y no el estado de Bell.

## Medición y orden

q0 se mide en c0 y q1 en c1; la cadena impresa es c1c0. Se rechazan conteos fuera de 00/11 y se comprueba el total. No se exige 512/512 porque la medición es un muestreo.

## Verificación adicional

La pureza reducida 1/2 se calcula desde el estado global puro sin mediciones. Esto evita concluir entrelazamiento solamente de una correlación clásica en Z. Es evidencia del modelo, no una prueba de Bell en hardware.

## Evidencia

La figura se guarda con identidad del estudiante y datos reales; el JSON conserva los conteos y pureza. El diagrama textual permite inspeccionar las conexiones sin instalar dependencias de dibujo adicionales.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
