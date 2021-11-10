from django.test import TestCase

from recipes.models import RecipeCard, Ingredient, MethodStep

class ModelTests(TestCase):
    """Tests RecipeCard model"""
    def setUp(self):
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

    def test_ingredient_foreign_key_relationship(self):
        """Ingredients foreign key relationship works with RecipeCard"""
        ingredient = Ingredient.objects.get(id = 1)
        self.assertEqual(ingredient.recipe.recipe_name, 'Test Recipe')

    def test_method_foreign_key_relationship(self):
        """MethodSteps foreign key relationship works with RecipeCard"""
        method = MethodStep.objects.get(id = 1)
        self.assertEqual(method.recipe.recipe_name, 'Test Recipe')


    