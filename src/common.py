"""Identidad, simulación reproducible, persistencia e histogramas sin escritorio."""
import json, os, platform, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import qiskit, qiskit_aer
from qiskit_aer import AerSimulator
SHOTS = 1024
SEED = 1152538
IDENTIDAD = 'Johan Barrera | 1152538 | Arquitectura de computadores'
ROOT = Path(os.environ.get('U12_OUTPUT', Path(sys.executable).resolve().parents[2] if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[1]))
def inicio(nombre):
    print('\n' + IDENTIDAD + '\nU12 — ' + nombre)
    print(f'CPU / AerSimulator | shots={SHOTS} | semilla={SEED}')
def simulator(noise_model=None):
    return AerSimulator(method='density_matrix', device='CPU', noise_model=noise_model, max_parallel_threads=1)
def counts(qc, shots=SHOTS, noise_model=None):
    return dict(simulator(noise_model).run(qc, shots=shots, seed_simulator=SEED).result().get_counts())
def save(name, data, qc=None):
    folder=ROOT/'resultados'; folder.mkdir(parents=True,exist_ok=True)
    data=dict(data, shots=SHOTS, seed=SEED)
    (folder/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    if qc is not None:
        (folder/(name+'_circuito.txt')).write_text(str(qc.draw(output='text',fold=100))+'\n')
    return data
def hist(series, titles, filename):
    fig, axes=plt.subplots(1,len(series),figsize=(6*len(series),4.8),squeeze=False)
    for ax, c, title in zip(axes[0],series,titles):
        states=['00','01','10','11']; n=sum(c.values())
        vals=[100*c.get(s,0)/n for s in states]
        bars=ax.bar(states,vals,color=['#187d9c','#6685ba','#b5a1d3','#e19b30'])
        ax.set(ylim=(0,112),ylabel='Frecuencia (%)',xlabel='Estado medido (q1 q0)',title=title)
        ax.spines[['top','right']].set_visible(False)
        for bar,s,v in zip(bars,states,vals):
            ax.text(bar.get_x()+bar.get_width()/2,v+2,f'{c.get(s,0)}\n{v:.2f}%',ha='center',fontsize=9)
    fig.suptitle('U12 · Simulación cuántica en CPU',fontsize=15,fontweight='bold')
    fig.text(.5,.02,IDENTIDAD+'\n1024 shots · semilla 1152538 · datos de simulación',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.10,1,.94))
    folder=ROOT/'capturas';folder.mkdir(parents=True,exist_ok=True)
    fig.savefig(folder/filename,dpi=160);plt.close(fig)
def entorno():
    return {'python':platform.python_version(),'qiskit':qiskit.__version__,'qiskit_aer':qiskit_aer.__version__,
            'sistema':platform.platform(),'arquitectura':platform.machine(),'libc':platform.libc_ver(),
            'metodo':'density_matrix','device':'CPU','semilla':SEED}
