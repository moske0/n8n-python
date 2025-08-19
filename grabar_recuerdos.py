import os

import sys

import json

from zep_utils import init_zep_client

from zep_cloud import EpisodeData

def grabar_recuerdos_batch(recuerdos_json_str):

    client, user_id = init_zep_client()

    try:

        lista_recuerdos = json.loads(recuerdos_json_str)

        if not isinstance(lista_recuerdos, list):

            raise ValueError("La entrada debe ser un string JSON que represente una lista.")

        episodes = []

        for recuerdo in lista_recuerdos:

            if not isinstance(recuerdo, dict) or "type" not in recuerdo or "data" not in recuerdo:

                continue

            episodes.append(EpisodeData(

                data=json.dumps(recuerdo["data"]) if isinstance(recuerdo["data"], dict) else recuerdo["data"],

                type=recuerdo["type"]

            ))

        if not episodes:

            print(json.dumps({"error": "No hay recuerdos válidos para grabar."}))

            sys.exit(1)

        client.graph.add_batch(episodes=episodes, user_id=user_id)

        print(json.dumps({"status": "éxito", "recuerdos_grabados": len(episodes)}))

    except Exception as e:

        print(json.dumps({"error": f"Ocurrió un error general: {e}"}))

        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) > 1:

        recuerdos = sys.argv[1]

        grabar_recuerdos_batch(recuerdos)

    else:

        print(json.dumps({"error": "No se proporcionó ningún lote de recuerdos en formato JSON."}))

        sys.exit(1)
