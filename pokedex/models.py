from django.db import models


class Pokemon(models.Model):
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=140, null=False)
    weight = models.IntegerField(null=False)
    height = models.IntegerField(null=False)
    
    def __str__(self):
        return self.name
    
class Trainer(models.Model):
    nameTrainer = models.CharField(max_length=40, null=False)
    lastname = models.CharField(max_length= 40, null=False)
    level = models.IntegerField(null=False)
    birthdate = models.DateField(null=False) 
    
    def __str__(self):
        return self.nameTrainer
    
    