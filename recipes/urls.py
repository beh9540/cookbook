'''
Created on Feb 21, 2013

@author: bhowell
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('recipes.views',
    url(r'^$', 'home', name='home'),
    url(r'^add$', 'add', name='recipe-new'),
    url(r'^(?P<recipe_id>\d+)/$', 'get', name='recipe-detail'),
    url(r'^update/(?P<recipe_id>[0-9]*)/$', 'update'),
    url(r'^review$', 'review'), 
)