from django.urls import path

from . import views

urlpatterns = [
    path(
        'recipes/index', 
        views.IndexView.as_view(),
        name = 'index'),
    path(
        'recipes/create_recipe', 
        views.create_recipe, 
        name = 'recipe'),
    path(
        'recipes/recipe_submitted/', 
        views.recipe_submitted, 
        name = 'recipe_submitted'),
    path(
        'recipes/display_recipe/', 
        views.display_recipe, 
        name = 'display_recipe'),

]