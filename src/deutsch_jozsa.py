"""Checkpoint 2: una consulta al oráculo bajo promesa constante/balanceada."""
from qiskit import QuantumCircuit
from common import SHOTS, inicio, counts, save, hist

def oracle_constante(n): return QuantumCircuit(n+1)
def oracle_balanceada(n):
    qc=QuantumCircuit(n+1)
    for i in range(n): qc.cx(i,n)
    return qc

def build_dj(oracle_qc,n=2):
    qc=QuantumCircuit(n+1,n);qc.x(n);qc.h(range(n+1))
    qc.compose(oracle_qc,inplace=True);qc.h(range(n));qc.measure(range(n),range(n));return qc

def deutsch_jozsa(oracle_qc,n=2,shots=SHOTS): return counts(build_dj(oracle_qc,n),shots)
def run():
    inicio('Deutsch–Jozsa');a=build_dj(oracle_constante(2));b=build_dj(oracle_balanceada(2))
    c=counts(a);d=counts(b)
    assert c=={'00':SHOTS};assert d=={'11':SHOTS}
    print('Constante f=0:',c);print('Balanceada f=x0 XOR x1:',d)
    print('Consultas: cuántico 1; clásico determinista hasta 3.');print(b.draw())
    hist([c,d],['Constante f=0','Balanceada: paridad'],'deutsch_jozsa.png')
    save('deutsch_jozsa',{'constante':c,'balanceada':d},b)
    save('dj_constante',{'counts':c},a)
    return c,d
if __name__=='__main__': run()
