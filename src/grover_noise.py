"""Checkpoint 4: mismo circuito, canales despolarizantes y probabilidad exacta."""
import math
from qiskit import transpile
from qiskit_aer.noise import NoiseModel, depolarizing_error
from grover import build_grover_circuit
from common import SHOTS, SEED, inicio, counts, simulator, save, hist

def build_noise_model(p1q=.001,p2q=.01):
    model=NoiseModel(basis_gates=['h','x','cz'])
    model.add_all_qubit_quantum_error(depolarizing_error(p1q,1),['h','x'])
    model.add_all_qubit_quantum_error(depolarizing_error(p2q,2),['cz'])
    return model

def exact_probabilities(qc,model):
    circuit=qc.remove_final_measurements(inplace=False);circuit.save_density_matrix()
    rho=simulator(model).run(circuit,shots=1,seed_simulator=SEED).result().data(0)['density_matrix']
    return {format(i,'02b'):float(p) for i,p in enumerate(rho.probabilities())}

def wilson(k,n):
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [mid-half,mid+half]

def grover_noise_experiment(target='11',shots=SHOTS):
    inicio('Grover con ruido')
    # Mantener puertas h/x/cz evita borrar el circuito o perder errores al cambiar de base.
    qc=transpile(build_grover_circuit(target),basis_gates=['h','x','cz'],optimization_level=0,seed_transpiler=SEED)
    model=build_noise_model();ideal=counts(qc,shots);noisy=counts(qc,shots,model)
    exact=exact_probabilities(qc,model);pi=ideal.get(target,0)/shots;pn=noisy.get(target,0)/shots
    ci=wilson(noisy.get(target,0),shots)
    print('Puertas:',dict(qc.count_ops()));print('Ideal:',ideal);print('Ruido:',noisy)
    print(f'Éxito ideal={100*pi:.4f}% | medido con ruido={100*pn:.4f}%')
    print(f'Degradación={100*(pi-pn):.4f} puntos porcentuales')
    print(f'Probabilidad exacta del modelo={100*exact[target]:.4f}%')
    print(f'IC Wilson 95%: [{100*ci[0]:.4f}%, {100*ci[1]:.4f}%]')
    hist([ideal,noisy],['Ideal','Despolarizante: λ1=.001, λ2=.01'],'grover_noise_comparison.png')
    save('grover_noise',{'target':target,'ideal':ideal,'noisy':noisy,'p_ideal':pi,'p_noisy':pn,
       'degradacion_pp':100*(pi-pn),'probabilidades_exactas':exact,'ic_wilson_95':ci,
       'lambda_1q':.001,'lambda_2q':.01,'operaciones':dict(qc.count_ops())},qc)
    return pi,pn
if __name__=='__main__': grover_noise_experiment()
