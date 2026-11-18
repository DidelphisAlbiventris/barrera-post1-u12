"""Checkpoint 1: Bell y contraste con el estado cuántico completo."""
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace
from common import SHOTS, inicio, counts, save, hist

def build_bell():
    qc=QuantumCircuit(2,2);qc.h(0);qc.cx(0,1);qc.measure([0,1],[0,1]);return qc

def bell_state_experiment(shots=SHOTS):
    inicio('Bell');qc=build_bell();c=counts(qc,shots)
    assert set(c)<= {'00','11'} and sum(c.values())==shots
    sv=Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
    # La pureza reducida 1/2 de un estado global puro confirma entrelazamiento.
    purity=float(partial_trace(sv,[1]).purity().real)
    assert abs(purity-.5)<1e-12
    print(c);print('Pureza reducida:',purity);print(qc.draw())
    hist([c],['Bell: correlación 00/11'],'bell_histogram.png')
    save('bell',{'counts':c,'pureza_reducida':purity},qc)
    return c
if __name__=='__main__': bell_state_experiment()
