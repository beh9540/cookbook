'''
Created on Feb 21, 2013

@author: bhowell
'''
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from recipes.models import Recipe, Ingredient, RecipeStep, Favorite
from recipes.forms import IngredientForm, RecipeForm, RecipeStepForm

@login_required
def home(request, items_per_page=25):
    '''Sets up the home page
    
    Gets a list of all the recipes, sets up a paginator for the recipes
    
    Args:
        request: the standard django.http.HttpRequest for all views
    
    Returns: 
        django.http.HttpResponse with a context containing a recipes variable
        for iteration of all the recipes
    '''
    recipe_list = Recipe.objects.all()
    page = request.GET.get('page')
    recipes = build_paginator(recipe_list, page, items_per_page)

    return render(request,'list.html', {
        "recipes": recipes,
        "page_name": 'Recipes',
    })

@login_required
def my_recipes(request, items_per_page=25):
    '''Gets the recipes for the current user
    
    Gets a list of all the recipes, and uses a paginator for the recipes
    
    Args:
        request: the standard django.http.HttpRequest for all views
        page: [optional] the page of the paginator to load
    
    Returns:
        django.http.HttpResponse with a context containing a recipes variable
        with a paginator
    '''
    recipe_list = Recipe.objects.filter(added_by=request.user)
    page = request.GET.get('page')
    recipes = build_paginator(recipe_list, page, items_per_page)
    
    return render(request,'list.html', {
        "recipes": recipes,
        "page_name": 'My Recipes',
    })

@login_required
def my_favorites(request, items_per_page=25):
    '''Gets the recipes for the current user
    
    Gets a lost of all the recipes, and uses a paginator for the recipes
    
    Args:
        request: the standard django.http.HttpRequest for all views
        page: [optional] the page of the paginator to load
    
    Returns:
        django.http.HttpResponse with a context containing a recipes variable
        with a paginator
    '''
    favorites = Favorite.objects.filter(user=request.user)
    recipe_list = [ f.recipe for f in favorites ]
    page = request.GET.get('page')
    recipes = build_paginator(recipe_list, page, items_per_page)
    
    return render(request,'list.html', {
        "recipes": recipes,
        "page_name": 'Favorites',
    })

@login_required
@permission_required('recipes.add_recipe')
def add(request):
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
        
    Returns:
        django.http.HttpResponse with a context containing a recipe_form,
        ingredient_formset and recipe_step_formset, or a redirect to the 
        list of recipes
    
    Raises: 
        django.http.Http404: recipe_id was given, but not a valid Recipe object
    '''
    
    IngredientFormSet = inlineformset_factory(Recipe,Ingredient,extra=1,
        form=IngredientForm)
    RecipeStepFormSet = inlineformset_factory(Recipe,RecipeStep,extra=1,
        form=RecipeStepForm)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, 
                prefix='recipe_id')
        if recipe_form.is_valid():
            recipe_id = recipe_form.save(commit=False)
            recipe_id.added_by = request.user
            recipe_id.save()
            ingredient_formset = IngredientFormSet(request.POST, 
                prefix='ingredients',instance=recipe_id)
            recipe_step_formset = RecipeStepFormSet(request.POST,
                prefix='recipe_steps',instance=recipe_id)
            if ingredient_formset.is_valid() and recipe_step_formset.is_valid():
                ingredient_formset.save()
                recipe_step_formset.save()
                return HttpResponseRedirect(reverse('home'))
    else:
        recipe_form = RecipeForm(prefix='recipe_id')
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        recipe_step_formset = RecipeStepFormSet(prefix='recipe_steps')
            
    return render(request, 'add.html', {
        'recipe_form' : recipe_form,                                
        'ingredient_formset' : ingredient_formset,
        'recipe_step_formset' : recipe_step_formset,
    })
    
@login_required
@permission_required('recipes.change_recipe')
def update(request, recipe):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'add.html', {
        'recipe_form' : recipe_form,                                
        'ingredient_formset' : ingredient_formset,
        'recipe_step_formset' : recipe_step_formset,
        })
    
@login_required
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
        IngredientFormSet = inlineformset_factory(Recipe,Ingredient,extra=1,
            form=IngredientForm)
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
        RecipeStepFormSet = inlineformset_factory(Recipe,RecipeStep,extra=1,
            form=RecipeStepForm)
        empty_form = RecipeStepFormSet(prefix='recipe_steps').empty_form
        return render(request, 'addRecipeStep.html', {'form': empty_form})
    else:
        return HttpResponseRedirect(reverse('home'))
    
@login_required
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
    try:
        recipe = Recipe.objects.select_related().get(pk=recipe_id)
    except Recipe.DoesNotExist:
        raise Http404
    ingredients = recipe.ingredient_set.all()
    ingredients = ingredients.order_by('number')
    steps = recipe.recipestep_set.all()
    steps = steps.order_by('number')
    return render(request, 'detail.html', {
       "recipe":recipe,
       "ingredients":ingredients,
       "steps":steps,
    })

def build_paginator(query_set, page, items_per_page):
    '''Encapsulates the construction of a paginator
    
    In order to encourage reuse, this function builds the paginator recipe for
    django.
    
    Args:
        query_set: the django query_set to paginate over
        page: the page number of the paginator to return
        items_per_page: an integer number for the items to put in the paginator
    
    Returns:
        django.core.paginator.Page for the query set containing the number
        of items requested in items_per_page
    '''
    paginator = Paginator(query_set, items_per_page)
    try:
        ret_paginator = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ret_paginator = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ret_paginator = paginator.page(paginator.num_pages)
    return ret_paginator

def build_ingredient(form,recipe,commit=True):
    '''Encapsulsates the logic in building an ingredient
    
    The inline model formset doesn't work in this case because we can't bind the
    recipe instance to the formset on instantiation. Therefore, we have to build
    the ingredient objects by hand.
    
    Args:
        form: The IngredientForm instance
        recipe: The Recipe object the foreign key will reference
        commit: whether or not the instance should be saved
    
    Returns:
        Ingredient for the form inputed, already saved unless save=False
    '''
    order = form.cleaned_data['number']
    amount = form.cleaned_data['amount']
    name = form.cleaned_data['name']
    unit = form.cleaned_data['unit']
    if 'id' in form.cleaned_data:
        id = form.cleaned_data['id']
        ingredient = Ingredient(id=id, amount=amount,name=name,unit=unit,
            recipe=recipe)
    else:
        ingredient = Ingredient(order=order,amount=amount,name=name,unit=unit,
            recipe=recipe)
    if commit:
        ingredient.save()
    return ingredient
    