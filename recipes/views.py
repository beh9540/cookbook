'''
Created on Feb 21, 2013

@author: bhowell
'''
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from models import Recipe, Ingredient, RecipeStep
from forms import IngredientForm, RecipeForm, RecipeStepForm


def home(request):
    '''Sets up the home page
    
    Gets a list of all the recipes, sets up a paginator for the recipes
    
    Args:
        request: the standard django.http.HttpRequest for all views
    
    Returns: 
        django.http.HttpResponse with a context containing a recipes variable
        for iteration of all the recipes
    '''
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 25)
    
    page = request.GET.get('page')
    
    try:
        recipes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recipes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recipes = paginator.page(paginator.num_pages)

    return render(request,'list.html', {"recipes": recipes})

def add(request, recipe_id=None):
    '''Adds a Recipe
    
    This view follows the create/update pattern for CRUD forms. A GET request
    returns an empty recipe form, ingredient formset, and recipe_step formset.
    A valid post creates the recipe object, builds the step and ingredient 
    objects from their respective formsets, and adds the foreign keys 
    references to the recipe. If the forms are not all valid, the function 
    returns attached references to all the forms/formsets. Finally, a GET 
    request with a valid recipe pk will return an attached form/formset for 
    updating the recipe.
    
    Args:
        request: the standard django.http.HttpRequest for all views
        recipe_id: pk of a recipe instance, defaults to None
        
    Returns:
        django.http.HttpResponse with a context containing a recipe_form,
        ingredient_formset and recipe_step_formset, or a redirect to the 
        list of recipes
    
    Raises: 
        django.http.Http404: recipe_id was given, but not a valid Recipe object
    '''
    IngrediantFormSet = formset_factory(IngredientForm)
    RecipeStepFormSet = formset_factory(RecipeStepForm)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, 
            prefix='recipe_id')
        ingredient_formset = IngrediantFormSet(request.POST, 
            prefix='ingredients')
        recipe_step_formset = RecipeStepFormSet(request.POST,
            prefix='recipe_steps')
        if ingredient_formset.is_valid() and recipe_form.is_valid() and\
            recipe_step_formset.is_valid():
            recipe_id = recipe_form.save()
            for ingredient_form in ingredient_formset.ordered_forms:
                order = ingredient_form.cleaned_data.order
                amount = ingredient_form.cleaned_data.amount
                name = ingredient_form.cleaned_data.name
                unit = ingredient_form.cleaned_data.unit
                Ingredient.objects.create(
                    order = order,
                    recipe_id = recipe_id,
                    amount = amount,
                    name = name,
                    unit = unit
                )
            for recipe_step_form in recipe_step_formset.ordered_forms:
                RecipeStep.objects.create(
                    order = recipe_step_form.cleaned_data.order,
                    recipe_id = recipe_id,
                    step = recipe_step_form.cleaned_data.step
                )
            return HttpResponseRedirect(reverse('home'))
    else:
        if not recipe_id:
            recipe_form = RecipeForm(prefix='recipe_id')
            ingredient_formset = IngrediantFormSet(prefix='ingredients')
            recipe_step_formset = RecipeStepFormSet(prefix='recipe_steps')
        else:
            recipe_id = get_object_or_404(Recipe, pk=recipe_id)
            initial_ingredients = [ ]
            initial_steps = [ ]
            for ingredient in recipe_id.ingredients:
                obj = {}
                obj['amount'] = ingredient.amount
                obj['unit'] = ingredient.unit
                obj['name'] = ingredient.name
                obj['order'] = ingredient.order
                initial_ingredients.append(obj)
            for step in recipe_id.steps:
                obj = {}
                obj['step'] = step.step
                obj['order'] = step.order
                initial_steps.append(obj)
            recipe_form = RecipeForm(instance=recipe_id)
            ingredient_formset = IngrediantFormSet(prefix='ingredients',
                initial=initial_ingredients)
            recipe_step_formset = RecipeStepFormSet(prefix='recipe_steps',
                initial=initial_steps)
        
    return render(request, 'add.html', {
        'recipe_form' : recipe_form,                                
        'ingredient_formset' : ingredient_formset,
        'recipe_step_formset' : recipe_step_formset,
    })

def new_ingredient_form(request):
    '''View for AJAX ingredient adding
    
    View for adding ingredients on the client using AJAX. The view checks to
    make sure the requester is using AJAX, then returns an empty 
    IngredientForm or redirects to home if the request is not AJAX
    
    Args:
        request: the standard django.http.HttpRequest for all views
    
    Returns:
        django.http.HttpResponse with a context containing an empty
        addIngredient form or a redirect to home
    
    '''
    if request.is_ajax():
        IngredientFormSet = formset_factory(IngredientForm)
        empty_form = IngredientFormSet(prefix='ingredients').empty_form
        return render(request, 'addIngredient.html', {'form': empty_form})
    else:
        return HttpResponseRedirect(reverse('home'))

def new_recipe_step_form(request):
    '''View for AJAX recipe_step adding
    
    View for adding steps to recipes on the client using AJAX. The view checks 
    to make sure the requester is using AJAX, then returns an empty 
    RecipeStepForm or redirects to home if the request is not AJAX
    
    Args:
        request: the standard django.http.HttpRequest for all views
    
    Returns:
        django.http.HttpResponse with a context containing an empty
        addIngredient form or a redirect to home
    
    '''
    if request.is_ajax():
        RecipeStepFormSet = formset_factory(RecipeStepForm)
        empty_form = RecipeStepFormSet(prefix='recipe_steps').empty_form
        return render(request, 'addRecipeStep.html', {'form': empty_form})
    else:
        return HttpResponseRedirect(reverse('home'))
    

def get(request, recipe_id):
    '''Detail view to view a single recipe
    
    Fulfills the Review part of CRUD, simply checks if recipe_id is a primary
    key to a recipe, and if it is returns a response containing the recipe
    instance and the detail.html template. If it is not a recipe pk, it 
    returns 404
    
    Args:
        request: the standard django.http.HttpRequest for all views
        recipe_id: pk of a recipe instance
    
    Returns:
        django.http.HttpResponse with a context containing a valid recipe 
        instance
    
    django.http.Http404: recipe_id was given, but not a valid Recipe object   
    '''
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'detail.html', {"recipe":recipe})
    