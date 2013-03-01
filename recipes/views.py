# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.formsets import formset_factory
from models import Recipe, Ingredient, RecipeStep
from forms import IngredientForm, RecipeForm, RecipeStepForm


def home(request):
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

    return render_to_response('list.html', {"recipes": recipes})

def add(request, recipe=None):
    IngrediantFormSet = formset_factory(IngredientForm, can_order=True)
    RecipeStepFormSet = formset_factory(RecipeStepForm, can_order=True)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, prefix='recipe')
        ingredient_formset = IngrediantFormSet(request.POST, 
            prefix='ingredients')
        recipe_step_formset = RecipeStepFormSet(request.POST,
            prefix='recipe_steps')
        if ingredient_formset.is_valid() and recipe_form.is_valid() and\
            recipe_step_formset.is_valid():
            recipe = recipe_form.save()
            for ingredient_form in ingredient_formset.ordered_forms:
                order = ingredient_form.cleaned_data.ORDER
                amount = ingredient_form.cleaned_data.amount
                name = ingredient_form.cleaned_data.name
                unit = ingredient_form.cleaned_data.unit
                Ingredient.objects.create(
                    order = order,
                    recipe = recipe,
                    amount = amount,
                    name = name,
                    unit = unit
                )
            for recipe_step_form in recipe_step_formset.ordered_forms:
                RecipeStep.objects.create(
                    order = recipe_step_form.cleaned_data.ORDER,
                    recipe = recipe,
                    step = recipe_step_form.cleaned_data.step
                )
            return HttpResponseRedirect('/recipes/')
    else:
        recipe_form = RecipeForm(prefix='recipe')
        ingredient_formset = IngrediantFormSet(prefix='ingredients')
        recipe_step_formset = RecipeStepFormSet(prefix='recipe_steps')
        
    return render_to_response('add.html', {
        'recipe_form' : recipe_form,                                
        'ingredient_formset' : ingredient_formset,
        'recipe_step_formset' : recipe_step_formset,
    })

def get(request, recipe_id):
    recipe = get_object_or_404(Recipe,pk=recipe_id)
    return render_to_response('detail.html', {"recipe":recipe})

def update(request, recipe_id):
    pass

def review(request):
    pass
    