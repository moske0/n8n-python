import sys
import os

print("--- INICIO DE LA PRUEBA DE IMPORTACIÓN ---")

# Imprimir variables de entorno relevantes
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
print(f"PATH: {os.environ.get('PATH')}")

# Definir la ruta de nuestros helpers
helpers_path = '/app/helpers'

print(f"\nDirectorio a añadir a la ruta: {helpers_path}")

# Añadir manualmente nuestro directorio de helpers a la ruta de Python
sys.path.append(helpers_path)

print("\nContenido de sys.path después de añadir la ruta:")
print(sys.path)

try:
    print(f"\nIntentando importar 'zep_helpers' desde {helpers_path}...")
    
    # Este es el import que falla en n8n
    from zep_helpers import get_zep_client_and_user
    
    print("\n**************************************************")
    print("*** ¡ÉXITO! Módulo 'zep_helpers' importado.   ***")
    print("**************************************************")
    print("Esto confirma que la imagen de Docker y la configuración de Python son CORRECTAS.")
    print("El problema reside exclusivamente en el entorno de ejecución del 'Code Node' de n8n.")

except ImportError as e:
    print("\n**************************************************")
    print("*** FALLO: No se pudo importar el módulo.      ***")
    print("**************************************************")
    print(f"Error detallado: {e}")
    print("Esto indicaría un problema fundamental en la imagen o los permisos, lo cual es muy extraño.")

except Exception as e:
    print(f"\nFALLO: Ocurrió un error inesperado. Error: {e}")

print("\n--- FIN DE LA PRUEBA DE IMPORTACIÓN ---")
