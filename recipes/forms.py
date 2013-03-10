'''
Created on Feb 21, 2013

@author: bhowell
'''
from django import forms
from models import Recipe,Unit
        
class IngredientForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    amount = forms.CharField(max_length=10,widget=forms.TextInput(attrs={
        'class':'input-block-level'}))
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), 
        required=False)
    name = forms.CharField(max_length=64,widget=forms.TextInput(attrs={
        'class':'input-block-level'}))
    number = forms.IntegerField(widget=forms.HiddenInput)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date_added','last_modified','added_by')
        widgets = {
            'description': forms.Textarea(attrs={'rows':'2',
                'class':'input-block-level'}),
        }

class RecipeStepForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    step = forms.CharField(widget=forms.Textarea(attrs={'rows':'2',
        'class':'input-block-level'}))
    number = forms.IntegerField(widget=forms.HiddenInput)