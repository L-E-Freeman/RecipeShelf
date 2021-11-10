from django.test import TestCase
from django.urls import reverse
from recipes.models import RecipeCard, Ingredient, MethodStep
from recipes.views import create_recipe

class IndexViewTests(TestCase):
    """Tests for recipe index page."""
     
    def create_recipe(self):
        """Set up non-modified objects used by all test methods."""
        # Object is receiving default values that can be changed when method 
        # is used 
        recipe = RecipeCard.objects.create(
            recipe_name = 'Test Recipe', 
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

    def test_no_recipes(self):
        """If no recipes exist, a message displays this."""
        response = self.client.get(reverse('recipes:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "No recipes currently available. Please create some!")

    def test_index_displays_single_recipe(self):
        """If a single recipe exists, display it on the index page."""
        recipe = create_recipe('Test 1')
        response = self.client.get(reverse('recipes:index'))
        self.assertQuerysetEqual(
            response.context['recipes'], [recipe]
        )

    def test_index_displays_multiple_recipes(self):
        """If multiple recipes exist, display them on the index page."""
        recipe = create_recipe('Test 1')
        recipe2 = create_recipe('Test 2')
        response = self.client.get(reverse('recipes:index'))
        # Ordered=False so I can compare a queryset to a list.
        self.assertQuerysetEqual(
            response.context['recipes'], [recipe, recipe2], ordered=False)

    def test_index_links_clickable(self):
        """
        When a recipe link is clicked, it should take you to the recipe
        display recipe page. 
        """
        recipe = create_recipe('Test 1')
        url = reverse('recipes:display_recipe', args = (recipe.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe)
