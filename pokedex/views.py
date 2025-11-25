from django.http import HttpResponse
from django.template import loader
from .models import Pokemon 
from .models import Trainer
from django.shortcuts import redirect, render
from pokedex.forms import PokemonForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import TrainerForm

def index(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'index.html', {'pokemons': pokemons})


def pokemon(request, id):
    pokemon = Pokemon.objects.get(id=id)
    return render(request, 'display_pokemon.html', {'pokemon': pokemon})



def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainer_list.html', {'trainers': trainers})



def trainer(request, id):
    trainer = Trainer.objects.get(id=id)
    return render(request, 'display_trainer.html', {'trainer': trainer})

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
