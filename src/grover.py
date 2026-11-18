"""Checkpoint 3: Grover para los cuatro objetivos, con orden q1q0 explícito."""
from qiskit import QuantumCircuit
from common import SHOTS, inicio, counts, save, hist

def build_grover_circuit(target='11'):
    if target not in ('00','01','10','11'): raise ValueError('Objetivo válido: 00, 01, 10 o 11')
    qc=QuantumCircuit(2,2);qc.h([0,1])
    # Qiskit imprime q1q0: el carácter derecho corresponde al qubit 0.
    zeros=[i for i,bit in enumerate(reversed(target)) if bit=='0']
    for i in zeros: qc.x(i)
    qc.cz(0,1)
    for i in zeros: qc.x(i)
    qc.h([0,1]);qc.x([0,1]);qc.cz(0,1);qc.x([0,1]);qc.h([0,1])
    qc.measure([0,1],[0,1]);return qc

def grover_2qubits(target='11',shots=SHOTS):
    qc=build_grover_circuit(target);c=counts(qc,shots)
    assert c=={target:shots},f'Grover incorrecto: {target}: {c}'
    print(f'Objetivo {target}: {c}; éxito={100*c[target]/shots:.2f}%')
    hist([c],[f'Grover: objetivo {target}'],'grover_'+target+'.png')
    save('grover_'+target,{'target':target,'counts':c},qc)
    return c

def run():
    inicio('Grover ideal')
    return {t:grover_2qubits(t) for t in ('00','01','10','11')}
if __name__=='__main__': run()
