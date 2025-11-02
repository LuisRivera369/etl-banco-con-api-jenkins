import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")  # Sube a la carpeta raiz del proyecto
sys.path.append(project_root)

from config.settings import DATA_READ_PATH
from config.settings import DATA_TRANSFORM_PATH
from config.settings import DATA_MERGE_PATH
from extraction.exchange_rate import get_tipo_de_cambio

"""
Realiza la limpieza, transformación y unión de datasets
"""
try:
    
    if not os.path.exists(DATA_READ_PATH):
        os.makedirs(DATA_READ_PATH)
        
    if not os.path.exists(DATA_TRANSFORM_PATH):
        os.makedirs(DATA_TRANSFORM_PATH)
    if not os.path.exists(DATA_MERGE_PATH):
        os.makedirs(DATA_MERGE_PATH)
        
    # Leer archivos READ CSV
    transacciones_read = pd.read_csv(DATA_READ_PATH + "/transacciones_read.csv")
    clientes_read = pd.read_csv(DATA_READ_PATH + "/clientes_read.csv")
    cuentas_read = pd.read_csv(DATA_READ_PATH + "/cuentas_read.csv")

    # Eliminar registros duplicados
    transacciones = transacciones_read.drop_duplicates().copy()
    clientes = clientes_read.drop_duplicates().copy()
    cuentas = cuentas_read.drop_duplicates().copy()

    # Rellenando datos vacios
    clientes["email"] = clientes["email"].fillna("SIN EMAIL")
    clientes["ingreso_mensual"] = clientes["ingreso_mensual"].fillna(0)
    clientes["riesgo_crediticio"] = clientes["riesgo_crediticio"].fillna("No Aplica")

    # ------------------------
    # Crear nuevas columnas:
    # ------------------------

    # Obtener tipo de cambio
    print("Obteniendo tipo de cambio USD/PEN...")

    USD_a_PEN = get_tipo_de_cambio()

    # Clientes: nuevas columnas:
    clientes["ingreso_mensual_usd"] = (clientes["ingreso_mensual"] / USD_a_PEN).round(2)
    clientes["ingreso_anual"] = clientes["ingreso_mensual"] * 12
    clientes["ingreso_anual_usd"] = clientes["ingreso_mensual_usd"] * 12

    # Transacciones: nueva columna monto_usd
    transacciones["monto_usd"] = (transacciones["monto"] / USD_a_PEN).round(2)
    # Cuentas: nueva columna saldo_usd
    cuentas["saldo_usd"] = (cuentas["saldo"] / USD_a_PEN).round(2)

    clientes.to_csv(
        os.path.join(DATA_TRANSFORM_PATH, "clientes_transform.csv"), index=False
    )
    transacciones.to_csv(
        os.path.join(DATA_TRANSFORM_PATH, "transacciones_transform.csv"), index=False
    )
    cuentas.to_csv(
        os.path.join(DATA_TRANSFORM_PATH, "cuentas_transform.csv"), index=False
    )
    print(f"Datos transformados guardados en: {DATA_TRANSFORM_PATH}")

    # -------------- MERGE - DATA ------------
    # Uniendo datasets en un solo dataset limpio
    transacciones_clientes = pd.merge(
        transacciones, clientes, on="id_cliente", how="inner"
    )
    data_merge = pd.merge(
        transacciones_clientes, cuentas, on=["id_cliente", "id_cuenta"], how="inner"
    )

    data_merge.to_csv(
        os.path.join(DATA_MERGE_PATH, "data_merge.csv"), index=False
    )

except Exception as e:
    print(f"Error al transformar los datos: {e}")
    sys.exit(1)