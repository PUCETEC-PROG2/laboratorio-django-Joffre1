from django import forms
from .models import Pokemon
from pokedex.models import Trainer


class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon 
        fields = "__all__"
        labels = {
            "name": "Nombre",
            "type": "Tipo",
            "weight": "Peso",
            "height": "Altura",
            "picture": "Imagen",
        }     
        
        widgets = {
            "name" : forms.TextInput(attrs={"class": "form-control"}),
            "type" : forms.TextInput (attrs={"class": "form-control"}),
            "height" : forms.NumberInput (attrs={"class": "form-control"}),
            "weight" : forms.NumberInput (attrs={"class": "form-control"}),
            "picture" : forms.ClearableFileInput (attrs={"class": "form-control"}),
        }
        
class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = "__all__"
        labels = {
        "nameTrainer": "Nombre", 
        "lastname": "Apellido", 
        "level": "Nivel", 
        "birthdate": "Fecha de cumpleaños", 
        "pictureTrainer": "Imagen"}

        widgets = {
            "nameTrainer": forms.TextInput(attrs={"class": "form-control"}),
            "lastname": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.NumberInput(attrs={"class": "form-control"}),
            "birthdate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }