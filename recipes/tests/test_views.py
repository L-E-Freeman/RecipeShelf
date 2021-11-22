from django.http import request
from django.test import TestCase
from django.urls import reverse
from recipes.models import RecipeCard, Ingredient, MethodStep
from django.contrib.auth.models import User
from django.contrib import auth


class IndexViewTests(TestCase):
    """Tests for recipe index page."""

    def setUp(self): 
        # Set up a user to use with all of the tests and log in the user.
        User.objects.create_user(username='temporary', password='temporary')
        self.client.login(username='temporary', password='temporary')

        User.objects.create_user(username='temporary2', password='temporary2')
     
    def create_recipe(self, recipe_name='Test Recipe', username='temporary'):
        """
        Creates a recipe with default values and a modifiable name to be used
        in tests.
        """
        # Object is receiving default values that can be changed when method 
        # is used 
        recipe = RecipeCard.objects.create(
            user = User.objects.get(username=username),
            recipe_name=recipe_name, 
            source = 'Test Source', 
            servings = 3,
            active_time_hours = 2,
            active_time_minutes = 15,
            total_time_hours = 2, 
            total_time_minutes = 15, 
            recipe_description = 'Test Description')
        recipe.save()

        ingredient = Ingredient.objects.create(
            ingredient_name = 'Test Ingredient',
            quantity = 1, 
            recipe = recipe)
        ingredient.save()

        method = MethodStep.objects.create(
            step = 'Test Step',
            recipe = recipe)
        method.save()

        # Make sure you return the created recipe object for use when method
        # is called in tests.
        return recipe

    def test_no_recipes(self):
        """If no recipes exist, a message displays this."""
        response = self.client.get(reverse('recipes:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "No recipes currently available. Please create some!")

    def test_index_displays_single_recipe(self):
        """If a single recipe exists, display it on the index page."""
        recipe = self.create_recipe(recipe_name='Test 1')
        
        response = self.client.get(reverse('recipes:index'))
        # Ordered=False so I can compare a queryset to a list.
        self.assertQuerysetEqual(
            # context object name in views is 'recipes', so we're using that 
            # here.
            response.context['recipes'], [recipe], ordered=False)

    def test_index_displays_multiple_recipes(self):
        """If multiple recipes exist, display them on the index page."""
        recipe = self.create_recipe(recipe_name='Test 1')
        recipe2 = self.create_recipe(recipe_name='Test 2')
        response = self.client.get(reverse('recipes:index'))
        self.assertQuerysetEqual(
            response.context['recipes'], [recipe, recipe2], ordered=False)

    def test_index_links_clickable(self):
        """
        When a recipe link is clicked, it should take you to the 
        display recipe page. 
        """
        recipe = self.create_recipe(recipe_name='Test 1')
        url = reverse('recipes:display_recipe', args = (recipe.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe)

    def test_logged_out_user_is_redirected_from_index(self):
        """
        A logged out user should not be able to access parts of site where 
        authentication is required.
        """
        self.client.logout()
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed('recipe_index.html')
        self.assertTemplateUsed('home_page.html')

    def test_user_can_only_access_own_recipes(self):
        """
        A user should only be able to access recipes they have created.
        """
        # temporary1 user already logged in via setUp().
        user_1_recipe = self.create_recipe(username=auth.get_user(self.client))
        self.client.logout()

        # Create new temp user and log in to create recipe and associate with 
        # temp2 user. 
        self.client.login(username='temporary2', password='temporary2')
        user_2_recipe = self.create_recipe(username=auth.get_user(self.client))

        # Response_owned is a recipe made by user 2 and should be viewable. 
        # Response_not_owned is recipe made by user 1 and should not be 
        # viewable.
        response_owned = self.client.get(
            reverse('recipes:display_recipe', args = (user_2_recipe.id,)))
        response_not_owned = self.client.get(
            reverse('recipes:display_recipe', args = (user_1_recipe.id,)))
        
        self.assertEqual(response_not_owned.status_code, 403)
        # Could either convert recipe.user to str, or use the user.username 
        # attribute to allow Django to compare properly.
        self.assertEqual(user_1_recipe.user.username, 'temporary')
        self.assertEqual(user_2_recipe.user.username, 'temporary2')
        self.assertEqual(response_owned.status_code, 200)
        

    def test_logout_view(self):
        """
        Check if the logout view truly logs out a logged in user.
        """
        response = self.client.get(reverse('recipes:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('home_page.html')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)