"""Entrada para el ejecutable Linux y para la ejecución desde Python."""
import argparse,json
from common import ROOT, entorno
import bell_state, deutsch_jozsa, grover, grover_noise

def main():
    parser=argparse.ArgumentParser(description='Laboratorio U12 · Johan Barrera · 1152538')
    parser.add_argument('experimento',nargs='?',default='todo',choices=['todo','bell','dj','grover','ruido','entorno'])
    args=parser.parse_args(); info=entorno();print(json.dumps(info,ensure_ascii=False,indent=2))
    if args.experimento=='entorno':return
    tasks={'bell':bell_state.bell_state_experiment,'dj':deutsch_jozsa.run,'grover':grover.run,'ruido':grover_noise.grover_noise_experiment}
    for name,fn in tasks.items():
        if args.experimento in ('todo',name):fn()
    folder=ROOT/'resultados';folder.mkdir(parents=True,exist_ok=True)
    (folder/'entorno.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    print('\nEjecución terminada. Resultados:',folder)
if __name__=='__main__':main()
