from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .forms import PokemonForm, TrainerForm
from .models import Pokemon, Trainer
from services.mongo_service import (clear_pokemon_details,get_pokemon_details, get_sync_logs,increase_views,update_pokemon_details,)
from services.sync_service import (sync_mongo_to_postgres,sync_postgres_to_mongo,)
from services.mongo import pokemon_details
from django.core.files.storage import FileSystemStorage
import os


def index(request):

    pokemons = Pokemon.objects.all().order_by("id")

    return render(
        request,
        "index.html",
        {
            "pokemons": pokemons
        }
    )

def pokemon(request, id: int):

    pokemon = Pokemon.objects.get(id=id)
    increase_views(id)
    mongo_data = get_pokemon_details(id)
    context = {
        "pokemon": pokemon,
        "mongo_data": mongo_data
    }
    template = loader.get_template("display_pokemon.html")
    return HttpResponse(template.render(context, request))



def trainer_list(request):
    trainers = Trainer.objects.all()

    return render(request, 'trainer_list.html', {'trainers': trainers})


def trainer(request, id: int):
    trainer = Trainer.objects.get(id=id)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_pokemon(request):
    if request.method == "POST":
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ("pokedex:index")
    else: 
        form = PokemonForm()

    return render (request, "pokemon_form.html", {"form":form})

@login_required
def edit_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    if request.method == "POST":
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect ("pokedex:index")
    else: 
        form = PokemonForm(instance=pokemon)

    return render (request, "pokemon_form.html", {"form":form})

@login_required
def delete_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id = pokemon_id)
    pokemon.delete()
    return redirect("pokedex:index")

class CustomLoginView(LoginView):

    template_name = 'login_form.html'

@login_required   
def add_trainer(request):
    if request.method == "POST":
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pokedex:trainer_list")
    else:
        form = TrainerForm()

    return render(request, "trainer_form.html", {"form": form})

@login_required
def edit_trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)

    if request.method == "POST":
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect("pokedex:trainer_list")
    else:
        form = TrainerForm(instance=trainer)

    return render(request, "trainer_form.html", {"form": form, "edit": True})

@login_required
def delete_trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    trainer.delete()
    return redirect("pokedex:trainer_list")


@login_required
def sync_postgres(request):

    try:

        cantidad = sync_postgres_to_mongo()

        messages.success(
            request,
            f"Se sincronizaron {cantidad} registros de PostgreSQL hacia MongoDB."
        )

    except Exception as e:

        messages.error(
            request,
            f"Error: {e}"
        )

    siguiente = request.GET.get("next")

    if siguiente == "mongo":
        return redirect("pokedex:mongo_index")

    return redirect("pokedex:index")


@login_required
def sync_mongo(request):

    try:

        cantidad = sync_mongo_to_postgres()

        messages.success(
            request,
            f"Se sincronizaron {cantidad} registros de MongoDB hacia PostgreSQL."
        )

    except Exception as e:

        messages.error(
            request,
            f"Error: {e}"
        )

    siguiente = request.GET.get("next")

    if siguiente == "mongo":
        return redirect("pokedex:mongo_index")

    return redirect("pokedex:index")

@login_required
def save_mongo_data(request, id):

    if request.method == "POST":

        favorite = "favorite" in request.POST

        comment = request.POST.get("comment", "")
        tags = request.POST.get("tags", "")
        update_pokemon_details(
    id,
    favorite,
    comment,
    tags
)
        return redirect("pokedex:pokemon", id=id)

@login_required
def clear_mongo_data(request, id):

    clear_pokemon_details(id)

    return redirect("pokedex:pokemon", id=id)

@login_required
def sync_logs_view(request):

    logs = get_sync_logs()

    return render(
        request,
        "sync_logs.html",
        {
            "logs": logs
        }
    )
    
    
from services.mongo import pokemon_details


@login_required
def mongo_index(request):

    pokemons = list(
        pokemon_details.find()
    )

    return render(
        request,
        "mongo_index.html",
        {
            "pokemons": pokemons
        }
    )
    
def mongo_pokemon(request, id):

    pokemon = pokemon_details.find_one({"pokemonId": id})

    if pokemon is None:
        messages.error(request, "No existe ese Pokémon en MongoDB.")
        return redirect("pokedex:mongo_index")

    return render(
        request,
        "mongo_display_pokemon.html",
        {
            "pokemon": pokemon
        }
    )
    
@login_required
def add_mongo_pokemon(request):

    if request.method == "POST":

        ruta_imagen = ""

        if "picture" in request.FILES:

            imagen = request.FILES["picture"]

            fs = FileSystemStorage(
                location=os.path.join("media", "pokemon_pictures")
            )

            nombre_archivo = fs.save(imagen.name, imagen)

            ruta_imagen = f"pokemon_pictures/{nombre_archivo}"

        favorite = "favorite" in request.POST

        comment = request.POST.get("comment", "")

        tags = request.POST.get("tags", "")

        lista_tags = []

        if tags.strip() != "":

            lista_tags = [
                tag.strip()
                for tag in tags.split(",")
                if tag.strip() != ""
            ]

        documento = {

            "pokemonId": pokemon_details.count_documents({}) + 1,

            "name": request.POST.get("name"),

            "type": request.POST.get("type"),

            "weight": int(request.POST.get("weight")),

            "height": int(request.POST.get("height")),

            "picture": ruta_imagen,

            "favorite": favorite,

            "comment": comment,

            "tags": lista_tags,

            "timesViewed": 0,

            "lastViewed": None

        }

        pokemon_details.insert_one(documento)

        messages.success(
            request,
            "Pokémon agregado correctamente en MongoDB."
        )

        return redirect("pokedex:mongo_index")

    return render(request, "mongo_form.html")

@login_required
def edit_mongo_pokemon(request, id):

    pokemon = pokemon_details.find_one(
        {"pokemonId": id}
    )

    if pokemon is None:

        messages.error(
            request,
            "No existe ese Pokémon."
        )

        return redirect("pokedex:mongo_index")

    if request.method == "POST":

        ruta_imagen = pokemon.get("picture", "")

        if request.FILES.get("picture"):

            imagen = request.FILES["picture"]

            fs = FileSystemStorage(
                location=os.path.join("media", "pokemon_pictures")
            )

            nombre = fs.save(imagen.name, imagen)

            ruta_imagen = f"pokemon_pictures/{nombre}"

        favorite = "favorite" in request.POST

        comment = request.POST.get("comment", "")

        tags = request.POST.get("tags", "")

        lista_tags = []

        if tags.strip():

            lista_tags = [
                tag.strip()
                for tag in tags.split(",")
                if tag.strip()
            ]

        pokemon_details.update_one(

            {"pokemonId": id},

            {
                "$set": {

                    "name": request.POST.get("name"),

                    "type": request.POST.get("type"),

                    "weight": int(request.POST.get("weight")),

                    "height": int(request.POST.get("height")),

                    "picture": ruta_imagen,

                    "favorite": favorite,

                    "comment": comment,

                    "tags": lista_tags

                }

            }

        )

        messages.success(
            request,
            "Pokémon actualizado correctamente."
        )

        return redirect("pokedex:mongo_index")

    return render(
        request,
        "mongo_form.html",
        {
            "pokemon": pokemon
        }
    )


@login_required
def delete_mongo_pokemon(request, id):

    pokemon = pokemon_details.find_one(
        {"pokemonId": id}
    )

    if pokemon is None:

        messages.error(
            request,
            "El Pokémon no existe."
        )

    else:

        pokemon_details.delete_one(
            {"pokemonId": id}
        )

        messages.success(
            request,
            "Pokémon eliminado correctamente de MongoDB."
        )

    return redirect("pokedex:mongo_index")

