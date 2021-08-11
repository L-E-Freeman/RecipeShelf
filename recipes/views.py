from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse

from .forms import (IngredientFormSet, MethodFormSet, RecipeForm)
from .models import RecipeCard

# Handles forms for creating recipe, both initialization and posting.
def create_recipe(request):
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

# View for returning the index, a list of all submitted recipes, with links 
# to view the recipe.
class IndexView(generic.ListView):
    model = RecipeCard
    template_name = 'recipes/recipe_index.html'
    context_object_name = 'recipes'

# View for returning the recipe submitted page, which confirms the recipe has 
# been submitted and redirects to the index page.
def recipe_submitted(request):
    return render(request, 'recipes/recipe_submitted.html',)

# TODO: Add a way to add a quantity to an ingredient. VVV

def display_recipe(request, recipecard_id): 
    recipe = get_object_or_404(RecipeCard, pk = recipecard_id)
    # Related name in models.py means you don't need to use ingredients_set, 
    # just ingredients.
    ingredients = recipe.ingredients.all()
    methods = recipe.steps.all()
    return render(request, 'recipes/display_recipe.html', {
        'recipe':recipe, 
        'ingredients': ingredients,
        'methods':methods})


