from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=140, null=False)
    weight = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    picture = models.ImageField(upload_to="pokemon_pictures/", null=True, blank=True)

    # Datos sincronizados desde MongoDB
    favorite = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default="")
    tags = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name
    
class Trainer(models.Model):
    nameTrainer = models.CharField(max_length=40, null=False)
    lastname = models.CharField(max_length= 40, null=False)
    level = models.IntegerField(null=False)
    birthdate = models.DateField(null=False) 
    pictureTrainer = models.ImageField(upload_to="trainer_picture/", null=True, blank=True)
    def __str__(self):
        return self.nameTrainer
    
    