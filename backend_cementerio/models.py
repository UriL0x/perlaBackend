from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=False)

# Estos 3 modelos, corresponden a una fila, cuadro(section) y manzana(block) 
class Block(models.Model):
    num = models.IntegerField(blank=False)
    
class Section(models.Model):
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True,blank=True)
    num = models.IntegerField(blank=False)
  
class Row(models.Model):
    num = models.IntegerField(blank=False)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True,blank=True)

class Grave(models.Model):
    row = models.ForeignKey(Row, on_delete=models.SET_NULL, null=True,blank=True)
    is_busy = models.BooleanField(default=False, blank=False)
    num = models.IntegerField(blank=False, unique=True)

class Dceasced(models.Model):
    name = models.CharField(max_length=255, blank=False)
    second_name = models.CharField(max_length=255, blank=False)
    date_of_death = models.DateField()
    grave = models.ForeignKey(Grave, on_delete=models.SET_NULL, null=True, blank=True)
    
class Document(models.Model):
    dceased = models.ForeignKey(Dceasced, on_delete=models.CASCADE)
    route = models.FileField(upload_to='./documents', blank=True)
    
