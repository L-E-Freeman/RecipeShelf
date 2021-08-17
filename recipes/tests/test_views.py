import datetime
from recipes.views import create_recipe
from django.test import TestCase
from django.urls import reverse
from recipes.models import RecipeCard


def create_recipe(recipe_name):
        return RecipeCard.objects.create(
            recipe_name = recipe_name,
            source = 'Test Source', 
            prep_time = datetime.timedelta(minutes = 20), 
            cooking_time = datetime.timedelta(minutes = 30), 
            servings = 3)

class IndexViewTests(TestCase):
    """Tests for recipe index page."""

    def test_no_recipes(self):
        """If no recipes exist, a message displays this."""
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes currently available.")

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
