# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render_to_response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.formsets import formset_factory
from models import Recipe
from forms import IngrediantForm, RecipeForm


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

def add(request):
    IngrediantFormSet = formset_factory(IngrediantForm, can_order=True)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, prefix='recipe')
        ingrediant_formset = IngrediantFormSet(request.POST, prefix='ingrediants')
        if ingrediant_formset.is_valid() and recipe_form.is_valid():
            recipe = recipe_form.save()
            for ingrediant_form in ingrediant_formset.ordered_forms:
                order = ingrediant_form.cleaned_data.ORDER
                amount = ingrediant_form.cleaned_data.amount
                name = ingrediant_form.cleaned_data.name
                unit = ingrediant_form.cleaned_data.unit
            return HttpResponseRedirect('/recipes/')
    else:
        recipe_form = RecipeForm()
        ingrediant_formset = IngrediantFormSet()
        
    return render_to_response('add.html', {
        'recipe_form' : recipe_form,                                
        'ingrediant_formset' : ingrediant_formset,
    })

def get(request, recipe_id):
    recipe = get_object_or_404(Recipe,pk=recipe_id)
    return render_to_response('detail.html', {"recipe":recipe})

def update(request, recipe_id):
    pass

def review(request):
    pass
    