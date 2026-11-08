# Bank Account Manager

[English version](README.md)

Módulo en Python para gestionar transferencias, depósitos y saldos bancarios, desarrollado en tres fases como trabajo de la asignatura Desarrollo de Software de la Universidad Carlos III de Madrid. Cada fase está en su propia carpeta, de modo que el repositorio muestra cómo se resolvió primero el problema, cómo se probó después con más rigor y cómo se reestructuró al final.

| Carpeta | Contenido |
|---|---|
| [`01-transaction-validation`](01-transaction-validation) | Script que lee una solicitud de transferencia en JSON y valida los dos IBAN |
| [`02-account-manager`](02-account-manager) | `AccountManager` con transferencias, depósitos y cálculo de saldo, desarrollado primero con pruebas y con el diseño de casos documentado |
| [`03-refactoring`](03-refactoring) | Las mismas funciones refactorizadas para que cada campo se valide a sí mismo, con el almacenamiento separado de la lógica de negocio |

Las tres trabajan con IBAN españoles (`ES` más 22 dígitos) y los comprueban con el algoritmo mod-97 de la norma ISO 13616.

## Ejecutar los tests

Cada carpeta es independiente. Hace falta Python 3.8 o superior; los tests de las carpetas 02 y 03 usan [`freezegun`](https://pypi.org/project/freezegun/) para fijar la fecha actual.

```bash
cd 01-transaction-validation
python -m unittest

cd ../02-account-manager        # igual para 03-refactoring
pip install freezegun
PYTHONPATH=src/main/python python -m unittest discover -s src/unittest/python -t src/unittest/python
```

En PowerShell de Windows, define la ruta con `$env:PYTHONPATH = "src/main/python"` antes del último comando. Las carpetas 02 y 03 incluyen además la configuración de PyBuilder (`build.py`, `pylintrc`) que se usó en la asignatura.

## Notas

- Es un trabajo académico: las reglas de validación (rango de importes, formato del concepto, fechas admitidas, formatos de fichero) vienen del enunciado, no de requisitos bancarios reales.
- Los códigos de transferencia son hashes MD5 y las firmas de depósito son hashes SHA-256, como pedía el enunciado. Sirven para identificar registros, no como mecanismo de seguridad.
