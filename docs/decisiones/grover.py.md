# Decisiones técnicas — `src/grover.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

P1-3: cuatro objetivos y éxito ideal superior a 90 %.

## Constructor compartido

build_grover_circuit es la única definición del circuito utilizada también por grover_noise.py. Así la comparación no mezcla algoritmos ni secuencias distintas.

## Endianness corregido

Se invierte la cadena objetivo al asignarla a índices de qubit. En Qiskit 01 significa q1=0, q0=1: se aplica X a q1 para que CZ marque esa amplitud. El ejemplo de la guía tenía intercambiados los casos 01 y 10.

## Una iteración

Con N=4 y una solución, θ=π/6 y sin²(3θ)=1. Un oráculo y un difusor bastan; repetir sin calcular el ángulo puede reducir la probabilidad.

## Validación y evidencia

Se rechazan objetivos fuera del dominio antes de simular. Los cuatro casos se validan por amplitud y por conteos ideales; cada uno produce JSON, diagrama y figura. No se oculta un error de orden probando únicamente 11.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
