"""
Script mejorado para grabar recuerdos en Zep Cloud con manejo robusto de errores y validaciones.
"""

import os
import sys
import json
import traceback
from typing import List, Dict, Any, Optional

# Importar módulos de Zep con manejo de errores
try:
    from zep_utils import init_zep_client
    from zep_cloud import EpisodeData
except ImportError as e:
    print(json.dumps({"error": f"No se pudieron importar los módulos de Zep: {str(e)}"}))
    sys.exit(1)

# Tipos de datos permitidos según la documentación de Zep
ALLOWED_TYPES = {"text", "json", "message"}

def validate_episode_data(episode: Dict[str, Any]) -> bool:
    """
    Valida que un episodio tenga el formato correcto.
    
    Args:
        episode: Diccionario con los datos del episodio
        
    Returns:
        bool: True si es válido, False si no
    """
    if not isinstance(episode, dict):
        return False
        
    if "type" not in episode or "data" not in episode:
        return False
        
    if not isinstance(episode["type"], str) or episode["type"] not in ALLOWED_TYPES:
        return False
        
    if episode["data"] is None:
        return False
        
    return True

def create_episode_data(episode: Dict[str, Any]) -> Optional[EpisodeData]:
    """
    Crea un objeto EpisodeData a partir de un diccionario.
    
    Args:
        episode: Diccionario con los datos del episodio
        
    Returns:
        EpisodeData: Objeto EpisodeData creado o None si hay error
    """
    try:
        # Si los datos son un diccionario, convertirlos a string JSON
        if isinstance(episode["data"], dict):
            data_str = json.dumps(episode["data"])
        else:
            data_str = str(episode["data"])
            
        return EpisodeData(
            data=data_str,
            type=episode["type"]
        )
    except Exception as e:
        print(json.dumps({
            "error": f"Error al crear EpisodeData: {str(e)}",
            "episode": episode
        }))
        return None

def log_error(message: str, exception: Optional[Exception] = None) -> None:
    """
    Registra errores en formato JSON para mejor trazabilidad.
    
    Args:
        message: Mensaje de error
        exception: Excepción opcional para incluir detalles
    """
    error_data = {"error": message}
    if exception:
        error_data["exception"] = str(exception)
        error_data["traceback"] = traceback.format_exc()
    print(json.dumps(error_data))

def grabar_recuerdos_batch(recuerdos_json_str: str) -> None:
    """
    Función principal para grabar un lote de recuerdos en Zep.
    
    Args:
        recuerdos_json_str: String JSON que representa una lista de recuerdos
    """
    try:
        # Validar entrada
        if not recuerdos_json_str or not recuerdos_json_str.strip():
            log_error("No se proporcionaron recuerdos (entrada vacía)")
            sys.exit(1)
            
        # Parsear JSON
        try:
            lista_recuerdos = json.loads(recuerdos_json_str)
        except json.JSONDecodeError as e:
            log_error(f"JSON inválido: {str(e)}")
            sys.exit(1)
            
        # Validar que sea una lista
        if not isinstance(lista_recuerdos, list):
            log_error("La entrada debe ser un string JSON que represente una lista")
            sys.exit(1)
            
        # Validar que la lista no esté vacía
        if not lista_recuerdos:
            log_error("La lista de recuerdos está vacía")
            sys.exit(1)
            
        # Inicializar cliente de Zep
        try:
            client, user_id = init_zep_client()
            if not client:
                log_error("No se pudo inicializar el cliente de Zep")
                sys.exit(1)
            if not user_id:
                log_error("No se pudo obtener el user_id")
                sys.exit(1)
        except Exception as e:
            log_error("Error al inicializar el cliente de Zep", e)
            sys.exit(1)
            
        # Procesar cada recuerdo
        episodes = []
        invalid_episodes = 0
        
        for i, recuerdo in enumerate(lista_recuerdos):
            # Validar formato del recuerdo
            if not validate_episode_data(recuerdo):
                print(json.dumps({
                    "warning": f"Recuerdo inválido en posición {i}: {recuerdo}"
                }))
                invalid_episodes += 1
                continue
                
            # Crear objeto EpisodeData
            episode = create_episode_data(recuerdo)
            if episode is None:
                print(json.dumps({
                    "warning": f"No se pudo crear EpisodeData para el recuerdo en posición {i}"
                }))
                invalid_episodes += 1
                continue
                
            episodes.append(episode)
            
        # Verificar si hay episodios válidos
        if not episodes:
            if invalid_episodes > 0:
                log_error(f"Ningún recuerdo válido. {invalid_episodes} recuerdos inválidos encontrados.")
            else:
                log_error("No hay recuerdos válidos para grabar.")
            sys.exit(1)
            
        # Grabar episodios en Zep
        try:
            result = client.graph.add_batch(episodes=episodes, user_id=user_id)
            
            # Preparar respuesta
            response = {
                "status": "éxito",
                "recuerdos_grabados": len(episodes)
            }
            
            if invalid_episodes > 0:
                response["recuerdos_omitidos"] = invalid_episodes
                
            # Si hay información adicional en el resultado, incluirla
            if hasattr(result, '__dict__'):
                result_dict = {k: v for k, v in result.__dict__.items() 
                             if not k.startswith('_') and v is not None}
                if result_dict:
                    response["resultados_adicionales"] = result_dict
                    
            print(json.dumps(response, ensure_ascii=False))
            
        except Exception as e:
            log_error(f"Error al grabar episodios en Zep: {str(e)}", e)
            sys.exit(1)
            
    except Exception as e:
        log_error("Ocurrió un error general en grabar_recuerdos_batch", e)
        sys.exit(1)

def main():
    """Función principal para manejar la ejecución del script"""
    try:
        # Verificar argumentos
        if len(sys.argv) < 2:
            print(json.dumps({
                "error": "No se proporcionó ningún lote de recuerdos en formato JSON.",
                "uso": "python grabar_recuerdos.py '[{\"type\": \"text\", \"data\": \"recuerdo\"}]'"
            }))
            sys.exit(1)
            
        # Obtener y procesar argumentos
        recuerdos_json_str = sys.argv[1]
        
        # Llamar a la función principal
        grabar_recuerdos_batch(recuerdos_json_str)
        
    except KeyboardInterrupt:
        print(json.dumps({"error": "Ejecución interrumpida por el usuario"}))
        sys.exit(1)
    except Exception as e:
        log_error("Error inesperado en la ejecución principal", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
