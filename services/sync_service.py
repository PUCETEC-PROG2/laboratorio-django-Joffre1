from pokedex.models import Pokemon
from services.mongo import pokemon_details, sync_logs
from datetime import datetime


def sync_postgres_to_mongo():

    pokemon_details.delete_many({})

    cantidad = 0

    for pokemon in Pokemon.objects.all():

        documento = {
            "pokemonId": pokemon.id,
            "name": pokemon.name,
            "type": pokemon.type,
            "weight": pokemon.weight,
            "height": pokemon.height,
            "picture": str(pokemon.picture),
            "favorite": False,
            "comment": "",
            "tags": [],
            "timesViewed": 0,
            "syncedAt": datetime.now()
        }

        pokemon_details.insert_one(documento)

        cantidad += 1

    sync_logs.insert_one({
        "date": datetime.now(),
        "origin": "PostgreSQL",
        "destination": "MongoDB",
        "records": cantidad,
        "status": "SUCCESS"
    })

    return cantidad