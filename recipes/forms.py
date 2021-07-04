from django import forms
from .models import Ingredient, RecipeCard
from django.forms import inlineformset_factory

class RecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeCard
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['recipe',]
    
IngredientFormSet = inlineformset_factory(
    RecipeCard, Ingredient, form = IngredientForm)