from rest_framework import serializers
from pokedex.models import Pokemon
from django.core.files.base import ContentFile
import base64

class PokemonSerializer(serializers.ModelSerializer):
    
    picture = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Pokemon
        fields = '__all__'
        
    def validate_picture(self, value):
        if value:
            try:
                format, imgstr = value.split(';base64,')
                ext = format.split('/')[-1]
                return ContentFile(
                    base64.b64decode(imgstr),
                    name=f'temp.{ext}'
                )
            except Exception:
                raise serializers.ValidationError("La imagen no se encuentra con base64 válida.")
        return value