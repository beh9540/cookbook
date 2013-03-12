'''
Created on Mar 12, 2013

@author: bhowell
Contains unit tests for the recipe models
'''
from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Category, Recipe
import time


class CategoryModelTest(TestCase):

    
    def test_create_no_parent(self):
        dinner = Category.objects.create(name='Test')
        
        qs = Category.objects.get(name='Test')
        
        self.assertEqual(dinner, qs)
        self.assertEqual(qs.name, 'Test')
        self.assertIsNone(qs.parent)
    
    def test_create_with_parent(self):
        parent = Category.objects.create(name='Parent')
        child1 = Category.objects.create(name='Child1', parent=parent)
        
        self.assertEqual(parent,child1.parent)
        self.assertIn(child1,parent.get_children())
        self.assertTrue(child1.is_leaf_node())
        self.assertFalse(child1.is_root_node())
        self.assertFalse(parent.is_leaf_node())
        self.assertTrue(parent.is_root_node())


class RecipeModelTest(TestCase):
    
    def setUp(self):
        self.test_user = 'test'
        self.test_password = 'password'
        self.user = User.objects.create_user(username=self.test_user, 
            password=self.test_password)
    
    def test_recipe_save(self):
        initial = Recipe.objects.create(name='Test',added_by=self.user)
        self.assertEqual(initial.date_added, initial.last_modified)
        time.sleep(10)
        initial.name = 'AwesomeTest'
        initial.save()
        later = Recipe.objects.get(pk=initial.pk)
        self.assertNotEqual(initial.date_added, initial.last_modified)
        self.assertNotEqual(later.last_modified, initial.last_modified)
        self.assertEqual(initial.date_added, later.date_added)
        