'''
Created on Feb 21, 2013

@author: bhowell
'''
from django import forms
from models import Ingrediant,Recipe
        
class IngrediantForm(forms.Form):
    amount = forms.CharField(max_length=10)
    unit = forms.CharField(max_length=64)
    name = forms.CharField(max_length=64)
        
class RecipeForm(forms.Form):
    class Meta:
        model = Recipe
        exclude = ('date_added',)
    