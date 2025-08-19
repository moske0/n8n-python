import os
from zep_cloud.client import Zep

def get_zep_client_and_user():
    """
    Inicializa el cliente de Zep y devuelve el cliente y el ID de usuario configurado.
    Lee la API Key y el User ID desde las variables de entorno.
    """
    api_key = os.environ.get("ZEP_API_KEY")
    user_id = os.environ.get("ZEP_USER_ID")

    if not api_key:
        raise ValueError("La variable de entorno ZEP_API_KEY no está configurada.")
    if not user_id:
        raise ValueError("La variable de entorno ZEP_USER_ID no está configurada. Debes crear tu usuario y guardar el ID.")
    
    client = Zep(api_key=api_key)
    
    # Devuelve tanto el cliente como el ID del usuario
    return client, user_id
