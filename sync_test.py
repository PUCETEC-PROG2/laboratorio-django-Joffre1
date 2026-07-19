import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()

from services.sync_service import sync_postgres_to_mongo

cantidad = sync_postgres_to_mongo()

print(f"Se sincronizaron {cantidad} Pokémon.")