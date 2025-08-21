#!/usr/bin/env python3
import os
import sys
import json
from serpapi import GoogleSearch

def search_local(query):
    # Obtener la API key desde las variables de entorno
    api_key = os.environ.get('SERPAPI_API_KEY')
    
    if not api_key:
        return {"error": "API key no encontrada en las variables de entorno"}
    
    # Configurar los parámetros de búsqueda
    params = {
        "engine": "google_local",
        "google_domain": "google.es",
        "q": query,
        "hl": "es",
        "gl": "es",
        "location": "Sanlucar la Mayor, Andalusia, Spain"
    }
    
    try:
        # Realizar la búsqueda
        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    except Exception as e:
        return {"error": str(e)}

# Si se ejecuta como script independiente
if __name__ == "__main__":
    # Verificar si se proporcionó un término de búsqueda como argumento
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "ayuntamiento"  # Valor por defecto
    
    results = search_local(query)
    print(json.dumps(results, indent=2, ensure_ascii=False))
