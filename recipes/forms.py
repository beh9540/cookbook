'''
Created on Feb 21, 2013

@author: bhowell
'''
from django import forms
from recipes.models import Recipe,Ingredient,RecipeStep
        
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        widgets = {
            'amount': forms.TextInput(attrs={'class':'input-block-level'}),
            'name': forms.TextInput(attrs={'class':'input-block-level'}),
            'number': forms.HiddenInput,
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date_added','last_modified','added_by')
        widgets = {
            'description': forms.Textarea(attrs={'rows':'2',
                'class':'input-block-level'}),
        }

class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        widgets = {
            'step': forms.Textarea(attrs={'rows':'2',
                'class':'input-block-level'}),
            'number': forms.HiddenInput,
        }