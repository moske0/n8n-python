#!/usr/bin/env python3
import os
import sys
import json
import serpapi

def search_google(query):
    # Obtener la API key desde las variables de entorno
    api_key = os.environ.get('SERPAPI_API_KEY')
    
    if not api_key:
        return {"error": "API key no encontrada en las variables de entorno"}
    
    # Configurar los parámetros de búsqueda
    params = {
        "engine": "google",
        "q": query,
        "location": "Sanlucar la Mayor, Andalusia, Spain",
        "google_domain": "google.es",
        "gl": "es",
        "hl": "es",
        "api_key": api_key
    }
    
    try:
        # Realizar la búsqueda
        results = serpapi.search(params)
        # Convertir el objeto SerpResults a un diccionario
        return dict(results)
    except Exception as e:
        return {"error": str(e)}

# Si se ejecuta como script independiente
if __name__ == "__main__":
    # Verificar si se proporcionó un término de búsqueda como argumento
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "Sanlúcar la Mayor"  # Valor por defecto
    
    results = search_google(query)
    print(json.dumps(results, indent=2, ensure_ascii=False))
