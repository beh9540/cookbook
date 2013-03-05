'''
Created on Feb 21, 2013

@author: bhowell

This file is for tests using the unittest module. These will pass
when you run "manage.py test".

'''

from django.test import TestCase


class ViewTest(TestCase):
    '''
    Tests for the view methods in this module
    '''
    def test_add_get(self):
        '''
        Tests the view.add function and corresponding urlconf
        '''
        response = self.client.get('/recipes/add')
        expected = 200
        self.assertEquals(response.status_code, expected)
    
    def test_add_post(self):
        '''
        Tests the view.add post of the form data
        '''
        response = self.client.post('/recipes/add', {
            'recipe-name' : u'Test Recipe',
            'recipe-description' : u'An awesome recipe',
            'ingredients-TOTAL_FORMS' : u'1',
            'ingredients-INITIAL_FORMS' : u'1',
            'ingredients-MAX_NUM_FORMS' : u'',
            'ingredients-0-amount' : u'1',
            'ingredients-0-unit' : u'cup',
            'ingredients-0-name' : u'foo',
            'ingredients-0-order' : u'0',
            'recipe_steps-TOTAL_FORMS' : u'0',
            'recipe_steps-INITIAL_FORMS' : u'1',
            'recipe_steps-MAX_NUM_FORMS' : u'',
            'recipe_steps-step' : u'Step foo for 42 minutes',
            'recipe_steps-order' : u'0'
        })
        self.assertRedirects(response, '/recipes/')
    
    def test_new_ingredient_form_ajax(self):
        '''
        Tests the ajax view newIngredientForm
        '''
        response = self.client.get('/recipes/newIngredient/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
    
    def test_new_ingredient_form(self):
        '''
        Tests the non-ajax response of newIngredientForm
        '''
        response = self.client.get('/recipes/newIngredient/')
        self.assertRedirects(response, '/recipes/')
    