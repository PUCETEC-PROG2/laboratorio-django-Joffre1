from django.http import HttpResponse
from django.template import loader
from .models import Pokemon 
from .models import Trainer

def index(request):
    pokemons = Pokemon.objects.all()
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def pokemon(request, id: int):
    pokemon = Pokemon.objects.get(id=id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))


def trainer_list(request):
    trainers = Trainer.objects.all()
    template = loader.get_template('trainer_list.html')
    return HttpResponse(template.render({'trainers': trainers}, request))


def trainer(request, id: int):
    trainer = Trainer.objects.get(id=id)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))
