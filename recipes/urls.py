from django.urls import path

from . import views

# URL patterns match what is typed in to the browser. If what is typed
# matches one of the strings here, the view is loaded.

app_name = 'recipes'
# TODO: Figure out why django is using the URL recipes/ 
# remember you have changed the form action on create recipe page.
urlpatterns = [
    path(
        '', 
        views.create_recipe),
    path(
        'recipes/index/', 
        views.IndexView.as_view(),
        name = 'index'),
    path(
        'recipes/create_recipe/', 
        views.create_recipe, 
        name = 'create_recipe'),
    path(
        'recipes/recipe_submitted/', 
        views.recipe_submitted, 
        name = 'recipe_submitted'),
    path(
        'recipes/display_recipe/<int:recipecard_id>', 
        views.display_recipe, 
        name = 'display_recipe'),

]