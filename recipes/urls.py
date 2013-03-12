'''
Created on Feb 21, 2013

@author: bhowell
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('recipes.views',
    #list URLs
    url(r'^$', 'home', name='home'),
    url(r'^user/$', 'my_recipes', name='recipe-user'),
    url(r'^favorites/$', 'my_favorites', name='recipe-fav'),
    #CRUD URLs
    url(r'^(?P<recipe_id>\d+)/$', 'get', name='recipe-detail'),
    url(r'^add/$', 'add', name='recipe-new'),
    url(r'^update/(?P<recipe>[0-9]+)/$', 'update', name='recipe-update'),
    url(r'^remove/$', 'remove', name='recipe-remove'),
    #AJAX URLs
    url(r'^newIngredient$', 'new_ingredient_form', 
        name='recipe-new-ingredient'),
    url(r'^newRecipeStep$', 'new_recipe_step_form', name='recipe-new-step')
)