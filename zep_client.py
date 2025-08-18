import os
from zep_cloud.client import Zep

# Obtén la clave API desde las variables de entorno
API_KEY = os.environ.get('ZEP_API_KEY')

if not API_KEY:
    print("Error: ZEP_API_KEY no está configurada en el entorno. Asegúrate de que el archivo .env esté cargado.")
else:
    try:
        # Inicializa el cliente Zep
        client = Zep(
            api_key=API_KEY,
        )
        print("Cliente Zep inicializado con éxito.")
        # Aquí puedes añadir cualquier otra lógica de tu aplicación que use el cliente Zep
        # Por ejemplo:
        # async def main():
        #     # ... usa el cliente aquí
        # await main()
    except Exception as e:
        print(f"Ocurrió un error al inicializar el cliente Zep: {e}")
