from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import IngredientForm, IngredientFormSet, RecipeForm

def make_recipe(request):
    if request.method == "GET":
        form = RecipeForm()
        formset = IngredientFormSet()
        # 2nd value is template to be used, 3rd value is a dictionary of values
        # to add to the template context. The template has a context of {form}
        # where values from RecipeForm() instance 'form' is used.
        return render(request, 'recipes/create_recipe.html', {
            'form':form, 
            'formset':formset})
    elif request.method == "POST":
        # Create form instance and add the data included in the form when 
        # submit button is pressed.
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
        formset = IngredientFormSet(request.POST, instance = recipe)
        if formset.is_valid():
            formset.save()
            return redirect('thanks')
        else:
            form = RecipeForm()
            formset = IngredientFormSet()
            return render(request, 'recipes/create_recipe.html', {
                'form':form, 
                'formset':formset})


def recipe_submitted(request):
    return render(request, 'recipes/recipe_submitted.html')
