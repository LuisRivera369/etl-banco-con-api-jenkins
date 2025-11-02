import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')   # Sube a la carpeta raiz del proyecto
sys.path.append(project_root)

from config.settings import DATA_PATH
from config.settings import DATA_READ_PATH

try:

    transacciones_file = os.path.join(DATA_PATH, "transacciones.json")
    clientes_file = os.path.join(DATA_PATH, "clientes.xlsx")
    cuentas_file = os.path.join(DATA_PATH, "cuentas.csv")

    if not os.path.exists(transacciones_file):
        raise FileNotFoundError(f"No se encontró: {transacciones_file}")
    if not os.path.exists(clientes_file):
        raise FileNotFoundError(f"No se encontró: {clientes_file}")
    if not os.path.exists(cuentas_file):
        raise FileNotFoundError(f"No se encontró: {cuentas_file}")

    transacciones = pd.read_json(transacciones_file)
    clientes = pd.read_excel(clientes_file)
    cuentas = pd.read_csv(cuentas_file)

    if not os.path.exists(DATA_READ_PATH):
        os.makedirs(DATA_READ_PATH)
    transacciones.to_csv(
        os.path.join(DATA_READ_PATH, "transacciones_read.csv"), index=False
    )
    clientes.to_csv(
        os.path.join(DATA_READ_PATH, "clientes_read.csv"), index=False
    )
    cuentas.to_csv(
        os.path.join(DATA_READ_PATH, "cuentas_read.csv"), index=False
    )
    print(f"Data read guardado en: {DATA_READ_PATH}")
    
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    sys.exit(1)