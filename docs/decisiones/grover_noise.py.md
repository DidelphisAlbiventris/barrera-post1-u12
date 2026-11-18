# Decisiones técnicas — `src/grover_noise.py`

Johan Barrera · 1152538 · Arquitectura de computadores

## Requerimiento cubierto

P1-4/5: comparación ideal/ruido con las tasas exigidas y justificación.

## Base sin optimización

Se fija H/X/CZ y optimization_level=0 para conservar las puertas a las que se asocia el ruido. Una optimización ideal puede cancelar operaciones o cambiar la base y alterar el experimento físico que se desea modelar.

## Canales del enunciado

Se mantienen λ1=0,001 y λ2=0,01, sin ruido de lectura. Se nombran parámetros de despolarización: no se confunden con probabilidades de error de Pauli o infidelidad media. El circuito 11 contiene 6 H, 4 X y 2 CZ.

## Método de matriz de densidad

Aer en CPU propaga el estado mixto de dos qubits eficientemente. El cálculo adicional antes de medir da una probabilidad exacta del modelo; los shots permiten mostrar fluctuación de muestreo.

## Comparación verificable

Se informa éxito, diferencia en puntos porcentuales y un intervalo de Wilson. Los 1002 éxitos no se sustituyen por el 89,4 % ilustrativo de la guía. La incertidumbre estadística no equivale a incertidumbre de calibración física.

## Verificación y alcance

La evidencia ejecutada está en `resultados/`, las pruebas en `tests/` y el alcance de plataforma en `docs/VERIFICACION.md`. Las capturas de la VM personal se incorporan después de ejecutar; no se confunden con los gráficos incluidos.
