# Componentes de terceros

La distribución ejecutable incorpora Python, Qiskit, Qiskit Aer, NumPy, SciPy, Matplotlib, SymEngine y otras bibliotecas; sus versiones están en requirements-lock.txt. Los avisos disponibles en los paquetes instalados se conservan en `docs/licencias_terceros/` y en los metadatos del paquete binario. El código académico no reclama autoría de estas bibliotecas.

Se utiliza PyInstaller 6.13.0 y sus hooks 2025.4 para empaquetar, no para cambiar el algoritmo. La biblioteca libstdc++ distribuida se reemplazó por una construcción compatible con glibc 2.17 proveniente del entorno de herramientas de construcción, evitando la dependencia glibc 2.38 del host. Se registran las comprobaciones y el hash en VERIFICACION y SHA256SUMS. libstdc++ pertenece a GCC y se distribuye bajo GPL con la GCC Runtime Library Exception; documentación y fuentes: https://gcc.gnu.org/libstdc++/ y https://www.gnu.org/licenses/gcc-exception-3.1.html .

Para reconstruir en otro Ubuntu se utiliza `scripts/compilar.sh`, que enlaza las bibliotecas de ese sistema. La compatibilidad resultante debe verificarse nuevamente; compilar sobre una distribución más reciente puede aumentar la versión mínima de glibc. No se incluye el paquete libc de Ubuntu usado temporalmente para comprobar compatibilidad.
