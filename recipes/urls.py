'''
Created on Feb 21, 2013

@author: bhowell
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('recipes.views',
    url(r'^$', 'home', name='home'),
    url(r'^add$', 'add', name='recipe-new'),
    url(r'^(?P<recipe_id>\d+)/$', 'get', name='recipe-detail'),
    url(r'^update/(?P<recipe>[0-9]*)/$', 'add', name='recipe-update'),
    url(r'^review$', 'review'), 
    url(r'^newIngredient$', 'new_ingredient_form', 
        name='recipe-new-ingredient'),
    url(r'^newRecipeStep$', 'new_recipe_step_form', name='recipe-new-step')
)