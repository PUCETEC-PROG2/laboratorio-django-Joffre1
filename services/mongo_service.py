from services.mongo import pokemon_details, sync_logs
from datetime import datetime


def get_pokemon_details(pokemon_id):

    documento = pokemon_details.find_one({"pokemonId": pokemon_id})

    if documento is None:

        documento = {
            "pokemonId": pokemon_id,
            "favorite": False,
            "comment": "",
            "tags": [],
            "timesViewed": 0,
            "lastViewed": None
        }

        pokemon_details.insert_one(documento)

    return documento


def increase_views(pokemon_id):

    pokemon_details.update_one(
        {"pokemonId": pokemon_id},
        {
            "$inc": {"timesViewed": 1},
            "$set": {"lastViewed": datetime.now()}
        }
    )
    
def update_pokemon_details(pokemon_id, favorite, comment, tags):

    lista_tags = []

    if tags.strip() != "":

        lista_tags = [
            tag.strip()
            for tag in tags.split(",")
            if tag.strip() != ""
        ]

    pokemon_details.update_one(
        {"pokemonId": pokemon_id},
        {
            "$set": {
                "favorite": favorite,
                "comment": comment,
                "tags": lista_tags
            }
        }
    )
    
def clear_pokemon_details(pokemon_id):
        pokemon_details.update_one(
        {"pokemonId": pokemon_id},
        {
            "$set": {
                "favorite": False,
                "comment": "",
                "tags": []
            }
        }
    )
        
def get_sync_logs():

    return sync_logs.find().sort("date", -1)