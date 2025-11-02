import os

# Configuración de conexión a SQL Server
SQL_SERVER = {
    "driver": "ODBC Driver 17 for SQL Server",
    "server": "localhost",
    "database": "BancoDB",
    "username": "sa",
    "password": "123456",
    "tabla": "transacciones_clientes",
}

# Obtiene la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define la ruta a la carpeta 'data_read' dentro de 'data'
DATA_PATH = os.path.join(BASE_DIR, "data")
DATA_READ_PATH = os.path.join(DATA_PATH, "data_read")
DATA_TRANSFORM_PATH = os.path.join(DATA_PATH, "data_transform")
DATA_MERGE_PATH = os.path.join(DATA_PATH, "data_merge")

OUTPUT_PATH = os.path.join(BASE_DIR, "output")
OUTPUT_GRAFICOS = os.path.join(OUTPUT_PATH, "graficos")

# API de tipo de cambio
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"
