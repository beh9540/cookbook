'''
Created on Mar 12, 2013

@author: bhowell
'''
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from recipes.models import Category, Unit

admin.site.register(Unit)
admin.site.register(Category,MPTTModelAdmin)