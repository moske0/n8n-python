import os
import sys
import json
import uuid
from zep_cloud.client import Zep

def crear_usuario():
    api_key = os.environ.get("ZEP_API_KEY")
    if not api_key:
        print(json.dumps({"error": "La variable de entorno ZEP_API_KEY no está configurada."}))
        sys.exit(1)

    client = Zep(api_key=api_key)

    user_id_permanente = "manolo_rodas_" + uuid.uuid4().hex[:12]
    datos_usuario = {
        "user_id": user_id_permanente,
        "email": "manuelrodas@gmail.com",
        "first_name": "Manuel",
        "last_name": "Rodas Morales",
        "metadata": {
            "description": "Usuario principal y propietario de este 'segundo cerebro'."
        }
    }

    try:
        usuario_creado = client.user.add(**datos_usuario)
        resultado = {
            "status": "PERFIL CREADO CON ÉXITO",
            "message": "Copia el siguiente user_id y guárdalo en Coolify como la variable de entorno ZEP_USER_ID.",
            "user_id": usuario_creado.user_id
        }
        print(json.dumps(resultado))
    except Exception as e:
        print(json.dumps({"error": f"No se pudo crear el usuario en Zep: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    crear_usuario()
