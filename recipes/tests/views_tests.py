'''
Created on Feb 21, 2013

@author: bhowell

This file is for tests using the unittest module. These will pass
when you run "manage.py test".

'''

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from recipes.models import Recipe,RecipeStep,Ingredient

class ViewTest(TestCase):
    '''
    Tests for the view methods in this module
    '''
    
    def setUp(self):
        '''
        Creates the test user for testing login and such, but no permissions
        '''
        self.test_user = 'test'
        self.test_password = 'password'
        self.user = User.objects.create_user(username=self.test_user, 
            password=self.test_password)
    
    def tearDown(self):
        self.client.logout()
        self.user.delete()
    
    def test_add_get(self):
        '''
        Tests the view.add function and corresponding urlconf
        '''
        permission = Permission.objects.get(codename='add_recipe')
        self.user.user_permissions.add(permission)
        self.client.login(username=self.test_user, password=self.test_password)
        response = self.client.get('/recipes/add/')
        self.assertTemplateUsed(response, template_name='add.html')
    
    def test_add_post(self):
        '''
        Tests the view.add post of the form data
        '''
        permission = Permission.objects.get(codename='add_recipe')
        self.user.user_permissions.add(permission)
        self.client.login(username=self.test_user, password=self.test_password)
        response = self.client.post('/recipes/add/', {
            'recipe-name' : u'Test Recipe',
            'recipe-description' : u'An awesome recipe',
            'recipe-categories' : u'4',
            'ingredients-TOTAL_FORMS' : u'1',
            'ingredients-INITIAL_FORMS' : u'0',
            'ingredients-MAX_NUM_FORMS' : u'',
            'ingredients-0-id' : u'',
            'ingredients-0-amount' : u'1',
            'ingredients-0-unit' : u'1',
            'ingredients-0-name' : u'foo',
            'ingredients-0-number' : u'0',
            'recipe_steps-TOTAL_FORMS' : u'1',
            'recipe_steps-INITIAL_FORMS' : u'0',
            'recipe_steps-MAX_NUM_FORMS' : u'',
            'recipe_steps-0-id' : u'',
            'recipe_steps-0-step' : u'Step foo for 42 minutes',
            'recipe_steps-0-number' : u'0',
        })
        self.assertTemplateNotUsed(response, template_name="add.html")
        self.assertRedirects(response, '/recipes/')
    
    def test_new_ingredient_form_ajax(self):
        '''
        Tests the ajax view newIngredientForm
        '''
        self.client.login(username=self.test_user, password=self.test_password)
        response = self.client.get('/recipes/newIngredient',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed(response, template_name="addIngredient.html")
    
    def test_new_ingredient_form(self):
        '''
        Tests the non-ajax response of newIngredientForm
        '''
        self.client.login(username=self.test_user, password=self.test_password)
        response = self.client.get('/recipes/newIngredient')
        self.assertRedirects(response, '/recipes/')
    
    def test_remove(self):
        '''
        Grants the test user recipe-remove, creates a test recipe, and then 
        tries to delete it using the remove url 
        '''
        permission = Permission.objects.get(codename='delete_recipe')
        self.user.user_permissions.add(permission)
        
        recipe = Recipe.objects.create(name='Test Recipe',
            description='An awesome recipe', added_by=self.user)
        ingredient = Ingredient.objects.create(name='Foo', amount=1, number=1,
            recipe=recipe)
        recipe_step = RecipeStep.objects.create(step='Add foo to the plate',
            number=1,recipe=recipe)
        
        self.client.login(username=self.test_user, password=self.test_password)
        response = self.client.get('/recipes/remove/',{
                'recipe': recipe.id,
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'Success')
        self.assertNotIn(recipe, Recipe.objects.all())
        self.assertNotIn(ingredient, Ingredient.objects.all())
        self.assertNotIn(recipe_step, RecipeStep.objects.all())
        
        
    