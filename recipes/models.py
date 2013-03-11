'''
Created on Feb 21, 2013

@author: bhowell
'''

from datetime import datetime
from django.db import models
from django.contrib.admin.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    picture = models.ImageField(blank=True, null=True, 
                                upload_to='pictures/%Y/%m/%d')
    date_added = models.DateTimeField()
    last_modified = models.DateTimeField()
    added_by = models.ForeignKey(User)
    
    def save(self,*args,**kwargs):
        now=datetime.now()
        if self.pk:
            self.last_modified = now
        else:
            self.date_added = now
            self.last_modified = now 
        super(Recipe,self).save(*args,**kwargs)
        
    def __unicode__(self):
        return self.name
        

class Ingredient(models.Model):
    recipe = models.ForeignKey('Recipe')
    amount = models.CharField(max_length=10)
    unit = models.ForeignKey('Unit',blank=True, null=True)
    name = models.CharField(max_length=64)
    number = models.PositiveSmallIntegerField()
    
    def __unicode__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=64)
    abbreviation = models.CharField(max_length=32)
    
    def __unicode__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey('Recipe')


class RecipeStep(models.Model):
    recipe = models.ForeignKey('Recipe')
    number = models.PositiveSmallIntegerField()
    step = models.TextField()