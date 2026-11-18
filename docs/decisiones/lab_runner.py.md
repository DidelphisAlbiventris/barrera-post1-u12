# Decisiones técnicas — `src/lab_runner.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

Punto de entrada ejecutable con experimentos independientes.

## Selección restringida

argparse acepta todo, bell, dj, grover, ruido y entorno. Los nombres inválidos producen ayuda y error, evitando ejecutar silenciosamente otro experimento.

## Fuentes reutilizadas

La entrada invoca las funciones de los cuatro archivos requeridos; no mantiene una segunda implementación que pueda divergir de lo que revisa el docente.

## Entorno visible

Se imprimen versiones, arquitectura y método antes de ejecutar. Esta información permite explicar diferencias entre máquinas y capturar evidencia de que se trabaja con Qiskit 1.x.

## Empaquetado

PyInstaller incluye el intérprete y bibliotecas para ejecutar sin instalación de Qiskit. No convierte la actividad en un programa DOS: conserva semántica Python y extensiones nativas dentro de una distribución Linux.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
