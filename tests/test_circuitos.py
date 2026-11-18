"""Verifica amplitudes, extremo sin ruido y extremo totalmente despolarizado."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from qiskit.quantum_info import Statevector,partial_trace
from bell_state import build_bell
from deutsch_jozsa import build_dj,oracle_constante,oracle_balanceada
from grover import build_grover_circuit
from grover_noise import build_noise_model,exact_probabilities
class Circuitos(unittest.TestCase):
    def test_bell_entrelazado(self):
        state=Statevector.from_instruction(build_bell().remove_final_measurements(inplace=False))
        self.assertAlmostEqual(abs(state.data[0])**2,.5)
        self.assertAlmostEqual(abs(state.data[3])**2,.5)
        self.assertAlmostEqual(partial_trace(state,[1]).purity().real,.5)
    def test_dj_promesa(self):
        for oracle,index in [(oracle_constante,0),(oracle_balanceada,3)]:
            state=Statevector.from_instruction(build_dj(oracle(2)).remove_final_measurements(inplace=False))
            self.assertAlmostEqual(state.probabilities(qargs=[0,1])[index],1.)
    def test_grover_cuatro_objetivos(self):
        for t in ['00','01','10','11']:
            with self.subTest(target=t):
                state=Statevector.from_instruction(build_grover_circuit(t).remove_final_measurements(inplace=False))
                self.assertAlmostEqual(state.probabilities()[int(t,2)],1.)
    def test_objetivo_invalido(self):
        with self.assertRaises(ValueError):build_grover_circuit('12')
    def test_limites_ruido(self):
        qc=build_grover_circuit('11')
        self.assertAlmostEqual(exact_probabilities(qc,build_noise_model(0,0))['11'],1.)
        for p in exact_probabilities(qc,build_noise_model(1,1)).values():self.assertAlmostEqual(p,.25)
    def test_ruido_configurado(self):
        qc=build_grover_circuit('11');p=exact_probabilities(qc,build_noise_model())
        self.assertAlmostEqual(sum(p.values()),1.)
        self.assertGreater(p['11'],.95);self.assertLess(p['11'],1.)
if __name__=='__main__':unittest.main(verbosity=2)
