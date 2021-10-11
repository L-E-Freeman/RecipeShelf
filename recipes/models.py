from django.db import models
from django.db.models.fields import DurationField
from django.contrib.auth.models import User

class RecipeCard(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name= 'recipe', 
        null=True)

    recipe_name = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    servings = models.IntegerField()

    active_time_hours = models.IntegerField()
    active_time_minutes = models.IntegerField()

    total_time_hours = models.IntegerField()
    total_time_minutes = models.IntegerField()
    
    recipe_description = models.TextField(max_length=200)

    # Displays the object as the recipe name. 
    def __str__(self):
        return self.recipe_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)

    # ForeignKey defines a relationship where a recipecard can have multiple
    # ingredients, but an ingredient only has one recipe.
    recipe = models.ForeignKey(
        RecipeCard, on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.ingredient_name

class MethodStep(models.Model):
    # Stops 'step' from appearing before text box on webpage.
    step = models.TextField(verbose_name="")

    recipe = models.ForeignKey(
        RecipeCard, on_delete=models.CASCADE, related_name="steps")

    def __str__(self):
        return self.step

