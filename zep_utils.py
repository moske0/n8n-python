import os
import sys
import json
from zep_cloud.client import Zep

def init_zep_client():
    """Inicializa y devuelve el cliente de Zep y el ID de usuario."""
    api_key = os.environ.get("ZEP_API_KEY")
    user_id = os.environ.get("ZEP_USER_ID")
    if not api_key or not user_id:
        print(json.dumps({"error": "Las variables de entorno ZEP_API_KEY y ZEP_USER_ID son necesarias."}))
        sys.exit(1)
    
    return Zep(api_key=api_key), user_id
