'''
Created on Feb 21, 2013

@author: bhowell
'''
from django import forms
from models import Recipe,Unit
        
class IngredientForm(forms.Form):
    amount = forms.CharField(max_length=10)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), 
        required=False)
    name = forms.CharField(max_length=64)
    order = forms.IntegerField(widget=forms.HiddenInput)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date_added','last_modified')

class RecipeStepForm(forms.Form):
    step = forms.CharField(widget=forms.Textarea)
    order = forms.IntegerField(widget=forms.HiddenInput)