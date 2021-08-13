from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from .forms import (IngredientFormSet, MethodFormSet, RecipeForm)
from .models import RecipeCard

# Handles forms for creating recipe, both initialization and posting.
def create_recipe(request):
    """Creates a form for recipe creation, including form initilization with 
    blank values, and saving the data with user entered values."""
    if request.method == "GET":
        form = RecipeForm()
        iformset = IngredientFormSet()
        mformset = MethodFormSet()
        # 2nd value is template to be used, 3rd value is a dictionary of values
        # to add to the template context. The template has a context of {form}
        # where values from RecipeForm() instance 'form' is used.
        return render(request, 'recipes/create_recipe.html', {
            'form':form, 
            'iformset':iformset, 
            'mformset':mformset,})
    elif request.method == "POST":
        # Create form instance and add the data included in the form when 
        # submit button is pressed. Check every form is valid and then save.
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe_card = form.save()
            iformset = IngredientFormSet(request.POST, instance = recipe_card)
            mformset = MethodFormSet(request.POST, instance = recipe_card)
        if form.is_valid() and iformset.is_valid() and mformset.is_valid():
            ingredients = iformset.save()
            methods = mformset.save()
            # Redirect to successful submission page.
            return HttpResponseRedirect(reverse('recipes:recipe_submitted'))
        else:
            # Rerender the form with an error message letting the user know 
            # a form isn't valid.
            form = RecipeForm() 
            iformset = IngredientFormSet()
            mformset = MethodFormSet()
            return render(request, 'recipes/create_recipe.html', {
                'form':form, 
                'iformset':iformset, 
                'mformset':mformset, 
                'error_message': "Oops! A form isn't valid."})

def edit_recipe(request, recipecard_id):
    """Allows a user to edit a recipe, the button for which is displayed on
    the recipe display page. The edit form is prepopulated with the data 
    which was previously entered by the user."""
    # Get instance of the object which the form will be displaying.
    recipe = get_object_or_404(RecipeCard, pk = recipecard_id)
    # Define the data for the initial population of the form with the data
    # already included in the object. 
    data = {
        'recipe_name':recipe.recipe_name, 
        'source':recipe.source, 
        'prep_time':recipe.prep_time, 
        'cooking_time':recipe.cooking_time, 
        'servings':recipe.servings}
    form = RecipeForm(initial = data)
    # Pass instance parameters to formsets.
    iformset= IngredientFormSet(instance = recipe)
    mformset = MethodFormSet(instance = recipe)

    # Displays form prepopulated with existing data.
    if request.method == "GET":
        return render(request, 'recipes/edit_recipe.html', {
                'form':form, 
                'iformset':iformset, 
                'mformset':mformset,})
    elif request.method == "POST":
        form = RecipeForm(request.POST, instance = recipe)
        iformset = IngredientFormSet(request.POST, instance = recipe)
        mformset = MethodFormSet(request.POST, instance = recipe)
        if form.is_valid() and iformset.is_valid() and mformset.is_valid():
            form.save()
            iformset.save()
            mformset.save()
            return HttpResponseRedirect(reverse(
                'recipes:edit_submitted', args = (recipecard_id,)))
        else:
            return HttpResponse("You've fucked it")

def recipe_submitted(request):
    """Redirect page the user sees once a new recipe has been submitted"""
    return render(request, 'recipes/recipe_submitted.html',)

def edit_submitted(request, recipecard_id):
    """Redirect page the user sees once an existing recipe has been edited."""
    return render(
        request, 
        'recipes/edit_submitted.html', 
        {'recipecard_id': recipecard_id})

class IndexView(generic.ListView):
    """Returns the index of existing user created recipes, with links to the
    recipes."""
    model = RecipeCard
    template_name = 'recipes/recipe_index.html'
    context_object_name = 'recipes'

def display_recipe(request, recipecard_id): 
    """Displays the details for a user created recipe."""
    recipe = get_object_or_404(RecipeCard, pk = recipecard_id)
    # Related name in models.py means you don't need to use ingredients_set, 
    # just ingredients.
    ingredients = recipe.ingredients.all()
    methods = recipe.steps.all()
    return render(request, 'recipes/display_recipe.html', {
        'recipe':recipe, 
        'ingredients': ingredients,
        'methods':methods})

