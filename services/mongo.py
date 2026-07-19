from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["pokedex_distribuida"]

pokemon_details = db["pokemon_details"]
sync_logs = db["sync_logs"]