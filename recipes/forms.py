'''
Created on Feb 21, 2013

@author: bhowell
'''
from django import forms
from models import Recipe,Unit
        
class IngredientForm(forms.Form):
    amount = forms.CharField(max_length=10)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), 
        empty_label=None)
    name = forms.CharField(max_length=64)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date_added',)

class RecipeStepForm(forms.Form):
    step = forms.TimeField()