import sqlalchemy
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")  # Sube a la carpeta raiz del proyecto
sys.path.append(project_root)

from config.settings import SQL_SERVER
from config.settings import DATA_MERGE_PATH


def get_connection_string():
    # Devuelve la cadena de conexión para SQLAlchemy.
    return (
        f"mssql+pyodbc://{SQL_SERVER['username']}:{SQL_SERVER['password']}"
        f"@{SQL_SERVER['server']}/{SQL_SERVER['database']}"
        f"?driver={SQL_SERVER['driver'].replace(' ', '+')}"
    )
try:
    # Carga los datos procesados en SQL Server.    
    data_merge = pd.read_csv(DATA_MERGE_PATH + "/data_merge.csv")
    conn_str = get_connection_string()
    engine = sqlalchemy.create_engine(conn_str)
    data_merge.to_sql(SQL_SERVER["tabla"], con=engine, if_exists="replace", index=False)
    print("Datos cargados exitosamente en SQL Server.")

except Exception as e:
    print(f"Error al cargar los datos: {e}")
    sys.exit(1)
