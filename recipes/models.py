from django.db import models
from django.db.models import Q

import re

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    picture = models.ImageField(blank=True, null=True, 
                                upload_to='pictures/%Y/%m/%d')
    date_added = models.DateTimeField()

class Ingrediant(models.Model):
    recipe = models.ForeignKey('Recipe')
    amount = models.CharField(max_length=10)
    unit = models.ForeignKey('Unit')
    name = models.CharField(max_length=64)

class Unit(models.Model):
    name = models.CharField(max_length=64)
    abbreviation = models.CharField(max_length=32)
    
    def findUnit(self, search_string):
        # first let's strip off any plurals or periods
        striped_search = str.rstrip('.s')
        units = Unit.objects.filter(Q(name__exact=search_string) | \
             Q(abbreviation__exact=search_string) | \
             Q(name__exact=striped_search) | \
             Q(abbreviation__exact=striped_search))
        if len(units) 
        

class RecipeStep(models.Model):
    recipe = models.ForeignKey('Recipe')
    order = models.PositiveSmallIntegerField()
    step = models.TextField()

class Review(models.Model):
    recipe = models.ForeignKey('Recipe')
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True, default='')
    