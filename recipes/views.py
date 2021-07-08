
from django.core.serializers.base import DeserializedObject
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.views import generic

from .forms import (IngredientForm, IngredientFormSet, MethodFormSet, 
RecipeForm)
from .models import RecipeCard

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
        if iformset.is_valid():
            ingredients = iformset.save()
        mformset = MethodFormSet(request.POST, instance = recipe_card)
        if mformset.is_valid():
            methods = mformset.save()
        if form.is_valid() and iformset.is_valid() and mformset.is_valid():
            # Redirect to successful submission page.
            # TODO:
                # have view button redirect to display_recipe view. Give 
                # display recipe view a way to access the saved form objects.
                # Potentially use a detailview here.
            return redirect('recipe_submitted')
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

def recipe_submitted(request):
    return render(request, 'recipes/recipe_submitted.html')

class IndexView(generic.ListView):
    model = RecipeCard
    template_name = 'recipes/recipe_index.html'
    context_object_name = 'recipes'

def display_recipe(request):
    
    return render(request, 'recipes/display_recipe.html', {
        'recipe_card':recipe_card,
    })