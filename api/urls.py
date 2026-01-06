from django.urls import path, include
from rest_framework import routers 
from .import views 

router = routers.DefaultRouter()
router.register(r'pokemons', views.PokemonViewSet)
router.register(r'trainers', views.TrainerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
