import os
from zep_cloud.client import Zep

def get_zep_client():
    """
    Inicializa y devuelve un cliente de Zep configurado.
    Lee la API Key desde las variables de entorno.
    """
    api_key = os.environ.get("ZEP_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno ZEP_API_KEY no está configurada.")
    
    client = Zep(api_key=api_key)
    return client
