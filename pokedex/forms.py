from django import forms
from .models import Pokemon

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
        