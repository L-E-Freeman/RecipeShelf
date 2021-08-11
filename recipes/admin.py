from django.contrib import admin

from .models import RecipeCard, Ingredient, MethodStep

class IngredientInLine(admin.TabularInline):
    model = Ingredient

class MethodStepInLine(admin.TabularInline):
    model = MethodStep

@admin.register(RecipeCard)
class RecipeCardAdmin(admin.ModelAdmin):
    inlines = [IngredientInLine, MethodStepInLine]

