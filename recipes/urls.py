from django.urls import path

from . import views

# URL patterns match what is typed in to the browser. If what is typed
# matches one of the strings here, the view is loaded.

app_name = 'recipes'
urlpatterns = [
    path(
        '', 
        views.homepage, 
        name = 'homepage'),
    path(
        'signup', 
        views.signup, 
        name = 'signup'),
    path(
        'login', 
        views.login_user, 
        name = 'login'),
    path(
        'logout', 
        views.logout_user, 
        name = 'logout'),
    path(
        'index', 
        views.IndexView.as_view(),
        name = 'index'),
    path(
        'create_recipe/', 
        views.create_recipe, 
        name = 'create_recipe'),
    path(
        'recipe_submitted/', 
        views.recipe_submitted, 
        name = 'recipe_submitted'),
    path(
        'display_recipe/<int:recipecard_id>', 
        views.display_recipe, 
        name = 'display_recipe'),
    path(
        'edit_recipe/<int:recipecard_id>', 
        views.edit_recipe, 
        name = 'edit_recipe'),
    path(
        'delete_recipe/<int:recipecard_id>',
        views.delete_recipe, 
        name = 'delete_recipe'),
    path(
        'edit_submitted/<int:recipecard_id>', 
        views.edit_submitted,
        name = 'edit_submitted'),
]