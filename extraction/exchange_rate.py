import requests
from config.settings import EXCHANGE_RATE_API
import sys
"""
Obtiene el tipo de cambio USD/PEN de la API.
"""

def get_tipo_de_cambio():
    try:
        response = requests.get(EXCHANGE_RATE_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['rates']['PEN']
    except Exception as e:
        print(f"Error al extraer tipo de cambio en API REST: {e}")
        sys.exit(1)
