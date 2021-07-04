from django.urls import path

from . import views

urlpatterns = [
    path('recipes/', views.make_recipe, name = 'recipe'),
    path('recipes/thanks/', views.recipe_submitted, name = 'thanks')

]