from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    picture = models.ImageField(blank=True, null=True, 
                                upload_to='pictures/%Y/%m/%d')
    date_added = models.DateTimeField()

class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe')
    amount = models.CharField(max_length=10)
    unit = models.ForeignKey('Unit',blank=True, null=True)
    name = models.CharField(max_length=64)
    order = models.PositiveSmallIntegerField()

class Unit(models.Model):
    name = models.CharField(max_length=64)
    abbreviation = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.name

class RecipeStep(models.Model):
    recipe = models.ForeignKey('Recipe')
    order = models.PositiveSmallIntegerField()
    step = models.TextField()

class Review(models.Model):
    recipe = models.ForeignKey('Recipe')
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True, default='')
    