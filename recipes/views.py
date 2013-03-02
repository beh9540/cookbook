# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404,render
from django.template import Context, Template
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

    return render(request,'list.html', {"recipes": recipes})

def add(request, recipe=None):
    IngrediantFormSet = formset_factory(IngredientForm, can_order=True, 
        can_delete=True)
    RecipeStepFormSet = formset_factory(RecipeStepForm, can_order=True, 
        can_delete=True)
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
        if not recipe:
            recipe_form = RecipeForm(prefix='recipe')
            ingredient_formset = IngrediantFormSet(prefix='ingredients')
            recipe_step_formset = RecipeStepFormSet(prefix='recipe_steps')
        else:
            recipe = get_object_or_404(Recipe,pk=recipe)
            initial_ingredients = [ ]
            initial_steps = [ ]
            for ingredient in recipe.ingredients:
                obj = {}
                obj['amount'] = ingredient.amount
                obj['unit'] = ingredient.unit
                obj['name'] = ingredient.name
                obj['ORDER'] = ingredient.order
                initial_ingredients.append(obj)
            for step in recipe.steps:
                obj = {}
                obj['step'] = step.step
                obj['ORDER'] = step.order
                initial_steps.append(obj)
            recipe_form = RecipeForm(instance=recipe)
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
    if request.is_ajax():
        IngredientFormSet = formset_factory(IngredientForm, can_order=True, 
            can_delete=True)
        empty_form = IngredientFormSet(prefix='ingredients').empty_form
        t = Template('''
            <tr>
            {{ form.order }}
            <td class='ingredient-amount'>{{ form.amount }}</td>
            <td>{{ form.unit }}</td>
            <td class='ingredient-name'>{{ form.name }}</td>
            <td><a class="remove-ingredient" href="">Remove</a></td>
            </tr>''')
        return HttpResponse(t.render(Context({'form': empty_form})))
    else:
        return HttpResponseRedirect('/recipes/')

def new_recipe_step_form(request):
    if request.is_ajax():
        RecipeStepFormSet = formset_factory(RecipeStepForm, can_order=True,
            can_delete=True)
        empty_form = RecipeStepFormSet(prefix='recipe_steps').empty_form
        t = Template('''
            {{ form.order }}
            <li>
                {{ form.step }}
                <a class="remove-step" href="">Remove</a>
            </li>
        ''')
        return HttpResponse(t.render(Context({'form': empty_form})))
    else:
        return HttpResponseRedirect('/recipes/')
    

def get(request, recipe_id):
    recipe = get_object_or_404(Recipe,pk=recipe_id)
    return render(request,'detail.html', {"recipe":recipe})

def update(request, recipe_id):
    pass

def review(request):
    pass
    