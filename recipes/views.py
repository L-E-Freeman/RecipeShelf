from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import (IngredientForm, IngredientFormSet, MethodFormSet, 
RecipeForm)

def make_recipe(request):
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
        # submit button is pressed.
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
        iformset = IngredientFormSet(request.POST, instance = recipe)
        if iformset.is_valid():
            iformset.save()
        mformset = MethodFormSet(request.POST, instance = recipe)
        if mformset.is_valid():
            mformset.save()
        if form.is_valid() and iformset.is_valid() and mformset.is_valid():
            return redirect('thanks')
        else:
            form = RecipeForm()
            iformset = IngredientFormSet()
            mformset = MethodFormSet()
            return render(request, 'recipes/create_recipe.html', {
                'form':form, 
                'iformset':iformset, 
                'mformset':mformset, 
                'error_message': "Oops! A form isn't valid."})


def recipe_submitted(request):
    return render(request, 'recipes/recipe_submitted.html')
