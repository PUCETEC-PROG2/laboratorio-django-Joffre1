from django.urls import path

from . import views

app_name = "pokedex"


urlpatterns = [
    path("", views.index, name="index"),
    path("pokemon/<int:id>/", views.pokemon, name="pokemon"),
    path("trainers/", views.trainer_list, name = "trainer_list"),
    path("trainersdetails/<int:id>", views.trainer, name ="trainer"),
    path("add_pokemon/", views.add_pokemon, name="add_pokemon"),
    path("edit_pokemon/<int:pokemon_id>", views.edit_pokemon, name="edit_pokemon"),
    path("delete_pokemon/<int:pokemon_id>", views.delete_pokemon, name="delete_pokemon"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("add_trainer/", views.add_trainer, name="add_trainer"),
    path("edit_trainer/<int:trainer_id>/", views.edit_trainer, name="edit_trainer"),
    path("delete_trainer/<int:trainer_id>/", views.delete_trainer, name="delete_trainer"),
    path(
    "sync/postgres-mongo/",
    views.sync_postgres,
    name="sync_postgres",
),

path(
    "sync/mongo-postgres/",
    views.sync_mongo,
    name="sync_mongo",
),
    path("pokemon/<int:id>/mongo/",views.save_mongo_data,name="save_mongo_data",),
    path("pokemon/<int:id>/clear-mongo/",views.clear_mongo_data,name="clear_mongo_data",),
    path("sync_logs/",views.sync_logs_view,name="sync_logs"),
    path("mongo/",views.mongo_index,name="mongo_index"),
    # CRUD MongoDB

path(
    "mongo/add/",
    views.add_mongo_pokemon,
    name="add_mongo_pokemon",
),

path(
    "mongo/<int:id>/",
    views.mongo_pokemon,
    name="mongo_pokemon",
),

path(
    "mongo/edit/<int:id>/",
    views.edit_mongo_pokemon,
    name="edit_mongo_pokemon",
),

path(
    "mongo/delete/<int:id>/",
    views.delete_mongo_pokemon,
    name="delete_mongo_pokemon",
),
]


