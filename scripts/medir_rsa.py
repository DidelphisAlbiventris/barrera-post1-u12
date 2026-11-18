"""Mide una muestra RSA-3072; destruye la clave temporal al terminar."""
import json,subprocess,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as d:
    key=Path(d)/'key.pem'
    subprocess.run(['openssl','genpkey','-algorithm','RSA','-pkeyopt','rsa_keygen_bits:3072','-out',str(key)],check=True,stderr=subprocess.DEVNULL)
    def run(args):return subprocess.check_output(['openssl']+args,stderr=subprocess.DEVNULL)
    pub=run(['pkey','-in',str(key),'-pubout','-outform','DER'])
    private=run(['rsa','-in',str(key),'-traditional','-outform','DER'])
    data={'modulus_bits':3072,'public_spki_der_bytes':len(pub),'private_pkcs1_der_bytes':len(private),'signature_bytes':384,'nota':'Muestra generada; DER privado varía entre claves. Ninguna clave privada se conserva.'}
    root=Path(__file__).resolve().parents[1]
    (root/'resultados/rsa_tamanos.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(data,ensure_ascii=False,indent=2))
