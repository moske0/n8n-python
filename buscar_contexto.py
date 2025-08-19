"""
Script estándar para buscar contexto relevante en Zep Cloud.
Versión corregida para manejar resultados None correctamente.
"""

import os
import sys
import json
from zep_utils import init_zep_client

# =========================
# CONFIGURACIÓN GENERAL
# =========================
MAX_RESULTS = 7    # Número máximo de resultados por tipo (edges, nodes, episodes)
DEFAULT_SCOPE = "all"    # Scope de búsqueda: "all" busca en edges, nodes y episodes
DEFAULT_RERANKER = "cross_encoder"    # Reranker recomendado por Zep para calidad global (ver docs): "cross_encoder"

# Filtros por tipo de nodo o edge (puedes dejar [] para no filtrar)
NODE_LABELS = []    # Ejemplo: ["Person", "Appointment", "Event"]
EDGE_TYPES = []    # Ejemplo: ["ATTENDED", "INVITED_TO"]
BFS_LASTN = 4    # BFS: cuántos episodios recientes usar como origen para priorizar contexto reciente (0 = desactivado)
MIN_RATING = None    # Filtrado por rating mínimo de hechos (None = sin filtrar, recomendado: None o 0.5+ si quieres solo hechos muy relevantes)

# =========================
# FIN DE CONFIGURACIÓN
# =========================

def buscar_contexto_global(user_query):
    client, user_id = init_zep_client()
    search_results = {}
    
    try:
        # Obtener episodios recientes para BFS si está activado
        bfs_uuids = None
        if BFS_LASTN and BFS_LASTN > 0:
            episodes_result = client.graph.episode.get_by_user_id(user_id=user_id, lastn=BFS_LASTN)
            # Verificar si episodes_result y episodes_result.episodes no son None
            if episodes_result and hasattr(episodes_result, 'episodes') and episodes_result.episodes:
                bfs_uuids = [ep.uuid_ for ep in episodes_result.episodes if getattr(ep, "role", None) == "user"]
        
        # Construir filtros de búsqueda
        search_filters = {}
        if NODE_LABELS:
            search_filters["node_labels"] = NODE_LABELS
        if EDGE_TYPES:
            search_filters["edge_types"] = EDGE_TYPES
        
        # Determinar scopes a buscar
        scopes = ["edges", "nodes", "episodes"] if DEFAULT_SCOPE == "all" else [DEFAULT_SCOPE]
        
        # Realizar búsquedas por scope
        for scope in scopes:
            try:
                res = client.graph.search(
                    user_id=user_id,
                    query=user_query,
                    scope=scope,
                    limit=MAX_RESULTS,
                    reranker=DEFAULT_RERANKER,
                    min_fact_rating=MIN_RATING if scope == "edges" else None,
                    search_filters=search_filters if search_filters else None,
                    bfs_origin_node_uuids=bfs_uuids if bfs_uuids else None
                )
                
                # Manejo seguro de resultados - verificar que no son None
                if scope == "edges":
                    search_results["edges"] = []
                    if hasattr(res, 'edges') and res.edges:
                        for e in res.edges:
                            search_results["edges"].append({
                                "fact": getattr(e, 'fact', ''),
                                "score": getattr(e, 'score', None),
                                "valid_at": getattr(e, 'valid_at', None),
                                "invalid_at": getattr(e, 'invalid_at', None)
                            })
                
                elif scope == "nodes":
                    search_results["nodes"] = []
                    if hasattr(res, 'nodes') and res.nodes:
                        for n in res.nodes:
                            search_results["nodes"].append({
                                "name": getattr(n, 'name', ''),
                                "summary": getattr(n, 'summary', ''),
                                "labels": getattr(n, 'labels', [])
                            })
                
                elif scope == "episodes":
                    search_results["episodes"] = []
                    if hasattr(res, 'episodes') and res.episodes:
                        for ep in res.episodes:
                            search_results["episodes"].append({
                                "summary": getattr(ep, 'summary', ''),
                                "created_at": getattr(ep, 'created_at', None)
                            })
                            
            except Exception as e:
                print(json.dumps({"error": f"Error en búsqueda {scope}: {str(e)}"}))
                continue
        
        # Construir el "context block" óptimo para IA
        context_block = build_context_block(search_results)
        print(context_block)
        
    except Exception as e:
        print(json.dumps({"error": f"No se pudo realizar la búsqueda: {str(e)}"}))
        sys.exit(1)

def build_context_block(results):
    """
    Construye un bloque de contexto óptimo para IA, combinando hechos, entidades y episodios relevantes.
    """
    block = []
    block.append("=== CONTEXTO RELEVANTE PARA LA TAREA ===\n")
    
    # Hechos (edges) - manejo seguro
    if "edges" in results and results["edges"]:
        block.append("HECHOS RELEVANTES (con fechas de validez):")
        for edge in results["edges"]:
            fact = edge.get("fact", "")
            if fact:  # Solo agregar si hay un hecho
                valid = edge.get("valid_at", "¿?")
                invalid = edge.get("invalid_at", "presente")
                block.append(f"- {fact} (Válido: {valid} - {invalid})")
        block.append("")
    
    # Entidades (nodes) - manejo seguro
    if "nodes" in results and results["nodes"]:
        block.append("ENTIDADES/RESÚMENES RELEVANTES:")
        for node in results["nodes"]:
            name = node.get("name", "")
            if name:  # Solo agregar si hay un nombre
                summary = node.get("summary", "")
                labels = ", ".join(node.get("labels", []))
                block.append(f"- {name} [{labels}]: {summary}")
        block.append("")
    
    # Episodios (episodes) - manejo seguro
    if "episodes" in results and results["episodes"]:
        block.append("EPISODIOS/MENSAJES RELEVANTES:")
        for ep in results["episodes"]:
            summary = ep.get("summary", "")
            if summary:  # Solo agregar si hay un resumen
                created = ep.get("created_at", "")
                block.append(f"- {summary} (Creado: {created})")
        block.append("")
    
    block.append("=== FIN DEL CONTEXTO ===")
    return "\n".join(block)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python buscar_contexto_global.py \"¿Cuál es la pregunta del usuario?\""}))
        sys.exit(1)
    
    user_query = sys.argv[1]
    buscar_contexto_global(user_query)
