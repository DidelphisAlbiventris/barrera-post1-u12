# Decisiones técnicas — `src/common.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

Soporte reproducible de todos los checkpoints.

## Centralizar parámetros

1024 shots y semilla 1152538 se definen en un lugar. La semilla corresponde al código del estudiante y permite repetir el muestreo en el mismo entorno, sin fingir que elimina la naturaleza probabilística del modelo.

## CPU explícita

device=CPU y un hilo son suficientes para dos o tres qubits, reducen dependencia de hardware y evitan exigir GPU NVIDIA, cuenta remota o Colab.

## Backend gráfico Agg

Las figuras se guardan sin servidor gráfico. Esto permite ejecutar en terminal o VM; xdg-open o Archivos se usa después para visualizarlas.

## Rutas y datos

Las salidas se ubican respecto de la raíz del proyecto, con U12_OUTPUT como redirección para pruebas aisladas. El ejecutable detecta su ubicación sin intentar escribir dentro del recurso temporal de PyInstaller.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
