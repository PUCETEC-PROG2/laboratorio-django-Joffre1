from pokedex.models import Pokemon
from services.mongo import pokemon_details, sync_logs
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
import os



def sync_postgres_to_mongo():

    errores_encontrados = 0
    errores_resueltos = 0
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

        if not pokemon.name:
            errores_encontrados += 1
            pokemon.name = "Sin nombre"
            errores_resueltos += 1

        if not pokemon.type:
            errores_encontrados += 1
            pokemon.type = "Desconocido"
            errores_resueltos += 1

        if pokemon.weight <= 0:
            errores_encontrados += 1
            pokemon.weight = 1
            errores_resueltos += 1

        if pokemon.height <= 0:
            errores_encontrados += 1
            pokemon.height = 1
            errores_resueltos += 1

        pokemon.save()

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

                "favorite": pokemon.favorite,
                "comment": pokemon.comment,
                "tags": (
                    pokemon.tags.split(",")
                    if pokemon.tags else []
                ),

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
        "status": "SUCCESS",
        "errorsFound": errores_encontrados,
        "errorsSolved": errores_resueltos

    })

    return cantidad

def sync_mongo_to_postgres():

    documentos = list(pokemon_details.find())

    errores_encontrados = 0
    errores_resueltos = 0
    cantidad = 0

    ids_mongo = [
        doc["pokemonId"]
        for doc in documentos
    ]

    Pokemon.objects.exclude(
        id__in=ids_mongo
    ).delete()

    for doc in documentos:

        # Validaciones
        if not doc.get("name"):
            errores_encontrados += 1
            doc["name"] = "Sin nombre"
            errores_resueltos += 1

        if not doc.get("type"):
            errores_encontrados += 1
            doc["type"] = "Desconocido"
            errores_resueltos += 1

        if doc.get("weight", 0) <= 0:
            errores_encontrados += 1
            doc["weight"] = 1
            errores_resueltos += 1

        if doc.get("height", 0) <= 0:
            errores_encontrados += 1
            doc["height"] = 1
            errores_resueltos += 1

    try:

        pokemon = Pokemon.objects.get(
        id=doc["pokemonId"]
        )

        pokemon.name = doc["name"]
        pokemon.type = doc["type"]
        pokemon.weight = doc["weight"]
        pokemon.height = doc["height"]

        if doc.get("picture"):
            pokemon.picture.name = doc["picture"]

        pokemon.favorite = doc.get("favorite", False)
        pokemon.comment = doc.get("comment", "")
        pokemon.tags = ", ".join(doc.get("tags", []))

        pokemon.save()

    except Pokemon.DoesNotExist:

        nuevo = Pokemon(

        id=doc["pokemonId"],
        name=doc["name"],
        type=doc["type"],
        weight=doc["weight"],
        height=doc["height"],
        favorite=doc.get("favorite", False),
        comment=doc.get("comment", ""),
        tags=", ".join(doc.get("tags", []))

    )

    if doc.get("picture"):
        nuevo.picture.name = doc["picture"]

        nuevo.save()

    cantidad += 1

    sync_logs.insert_one({

        "date": datetime.now(),

        "origin": "MongoDB",

        "destination": "PostgreSQL",

        "records": cantidad,

        "status": "SUCCESS",

        "errorsFound": errores_encontrados,

        "errorsSolved": errores_resueltos

    })

    return cantidad

def get_sync_logs():

    logs = list(
        sync_logs.find().sort("date", -1)
    )

    return logs