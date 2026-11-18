# Decisiones de infraestructura y archivos auxiliares

Johan Barrera · 1152538 · Arquitectura de computadores

| Archivo | Decisión y justificación | Comprobación |
|---|---|---|
| `ejecutar.sh` | Ubica la raíz y prioriza la distribución binaria; permite ejecutar por checkpoint. Usa salida explícita si no hay binario ni entorno. | Se ejecutan entorno y todos los experimentos. |
| `instalar.sh` | Usa un entorno virtual para no modificar el Python del sistema; fija dependencias académicas. | Instalación aislada y pruebas de fuentes. |
| `requirements.txt` | Versiones verificadas, Qiskit 1.x; evita cambios de API por instalación sin versión. | Se compara con entorno registrado. |
| `requirements-lock.txt` | Registro completo de dependencias del entorno de construcción. | `pip freeze`, sin presentarlo como universal para todo Python. |
| `scripts/compilar.sh` | PyInstaller onedir, con módulos dinámicos Qiskit/Aer. El directorio acompaña al ejecutable. | Prueba del ejecutable fuera del entorno virtual. |
| `scripts/medir_rsa.py` | OpenSSL genera una muestra temporal para medir DER sin inventar tamaños de claves. Elimina secretos al salir. | Resultado JSON con formato y longitud. |
| `.gitignore` | Excluye binarios grandes, cachés y entorno virtual; fuentes y figuras permanecen versionables. | `git status` antes de cada commit. |
| `README.md` | Incluye resultados reales, cuatro circuitos, decisiones P1 y vínculos a P2. | Matriz de requisitos y revisión de enlaces. |
| `docs/GUIA_CAPTURAS.md` | Indica acción, contenido visible y nombre de cada evidencia propia. | No se generan pantallas ficticias de VirtualBox. |
| `docs/COMMITS.md` | Ofrece commits de revisión por checkpoint y tres etapas de P2. | No se fabrica historia Git ni fechas anteriores. |
| `docs/etapas_pqc/*.md` | Copias progresivas para organizar la revisión del documento. Están excluidas de Git. | La etapa final coincide con el análisis completo. |
| `resultados/*.json` | Persistencia de conteos y parámetros, sin necesidad de leer datos desde una imagen. | Sumas de shots y concordancia con las figuras. |
| `resultados/*_circuito.txt` | Dibujo emitido por Qiskit; no se necesita LaTeX ni pylatexenc. | Comparación con constructor de cada circuito. |
| `capturas/*.png` | Histogramas reales con identidad, semilla y eje porcentual común. | Revisión visual de etiquetas y recuentos. |
| `bin/u12_lab/` | Intérprete y dependencias empaquetados para Linux x86_64, sin instalación adicional de Qiskit. | Alcance exacto en VERIFICACION.md; no prometer todas las distribuciones. |

Los Markdown de decisiones forman una explicación complementaria, no sustituyen las cuatro decisiones mínimas que permanecen en los archivos exigidos por la rúbrica: dos en README y dos en analisis-pqc.md.
