import os
import sys
import json
from serpapi import GoogleSearch

def search_amazon_products(search_term):
    # Obtener la API key desde las variables de entorno
    api_key = os.environ.get('SERPAPI_API_KEY')
    
    if not api_key:
        return {"error": "API key no encontrada en las variables de entorno"}
    
    # Configurar los parámetros de búsqueda
    params = {
        "engine": "amazon",
        "k": search_term,
        "language": "amazon.es|es_ES",
        "amazon_domain": "amazon.es",
        "delivery_zip": "41800",
        "shipping_location": "ES",
        "s": "exact-aware-popularity-rank"
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
    if len(sys.argv) > 1:
        search_term = sys.argv[1]
    else:
        search_term = "ofertas"
    
    results = search_amazon_products(search_term)
    print(json.dumps(results))
