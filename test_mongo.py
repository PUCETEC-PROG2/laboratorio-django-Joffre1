from services.mongo import pokemon_details

pokemon_details.insert_one({
    "pokemonId": 1,
    "favorite": False,
    "comment": "Conexión exitosa",
    "tags": [],
    "timesViewed": 0
})

print("Documento insertado correctamente")