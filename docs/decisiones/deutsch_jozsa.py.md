# Decisiones técnicas — `src/deutsch_jozsa.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

P1-2: dos oráculos n=2 y explicación de una consulta frente a tres.

## Oráculos explícitos

La identidad representa f=0; dos CX hacia la ancilla representan paridad x0 XOR x1, que es balanceada. El código no consulta una tabla clásica para decidir el resultado.

## Ancilla en menos

X seguida de H prepara |−⟩. El oráculo produce retroceso de fase, y la segunda capa H permite distinguir constante de balanceada. Se mide solo el registro de entrada.

## Asserts completos

Se exige exactamente 1024 mediciones 00 para la constante y 1024 mediciones 11 para esta paridad. Comprobar solamente que aparece 00 dejaría pasar distribuciones incorrectas.

## Límite de la comparación

Una composición del circuito oráculo cuenta como una consulta aunque internamente contenga dos CX. Las tres consultas clásicas corresponden al peor caso determinista exacto bajo promesa; no se atribuye una aceleración de tiempo de ejecución a Python.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
