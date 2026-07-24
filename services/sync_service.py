from pokedex.models import Pokemon
from services.mongo import pokemon_details, sync_logs
from datetime import datetime



def sync_postgres_to_mongo():

    cantidad = 0
    
    ids_postgres = [
    pokemon.id
    for pokemon in Pokemon.objects.all()
]
    
    pokemon_details.delete_many({
    "pokemonId": {
        "$nin": ids_postgres
    }
})

    for pokemon in Pokemon.objects.all():

        documento_existente = pokemon_details.find_one(
            {"pokemonId": pokemon.id}
        )

        if documento_existente:

            pokemon_details.update_one(
                {"pokemonId": pokemon.id},
                {
                    "$set": {
                        "name": pokemon.name,
                        "type": pokemon.type,
                        "weight": pokemon.weight,
                        "height": pokemon.height,
                        "picture": str(pokemon.picture),
                        "syncedAt": datetime.now()
                    }
                }
            )

        else:

            pokemon_details.insert_one({

                "pokemonId": pokemon.id,
                "name": pokemon.name,
                "type": pokemon.type,
                "weight": pokemon.weight,
                "height": pokemon.height,
                "picture": str(pokemon.picture),

                "favorite": pokemon.favorite,
                "comment": pokemon.comment,
                "tags": (
                    pokemon.tags.split(",")
                    if pokemon.tags else []
                ),

                "timesViewed": 0,
                "lastViewed": None,
                "syncedAt": datetime.now()

            })

        cantidad += 1

    sync_logs.insert_one({

        "date": datetime.now(),
        "origin": "PostgreSQL",
        "destination": "MongoDB",
        "records": cantidad,
        "status": "SUCCESS"

    })

    return cantidad

def sync_mongo_to_postgres():

    documentos = pokemon_details.find()

    cantidad = 0

    for doc in documentos:

        try:

            pokemon = Pokemon.objects.get(id=doc["pokemonId"])

            pokemon.favorite = doc.get("favorite", False)
            pokemon.comment = doc.get("comment", "")

            pokemon.tags = ", ".join(
                doc.get("tags", [])
            )

            pokemon.save()

            cantidad += 1

        except Pokemon.DoesNotExist:
            pass

    sync_logs.insert_one({

        "date": datetime.now(),
        "origin": "MongoDB",
        "destination": "PostgreSQL",
        "records": cantidad,
        "status": "SUCCESS"

    })

    return cantidad

def get_sync_logs():

    logs = list(
        sync_logs.find().sort("date", -1)
    )

    return logs