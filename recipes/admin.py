from recipes.forms import IngredientFormSet
from django.contrib import admin

from .models import RecipeCard, Ingredient

class IngredientInLine(admin.TabularInline):
    model = Ingredient

@admin.register(RecipeCard)
class RecipeCardAdmin(admin.ModelAdmin):
    inlines = [IngredientInLine,]
