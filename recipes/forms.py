from django import forms
from .models import Ingredient, MethodStep, RecipeCard
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
    RecipeCard, Ingredient, form = IngredientForm, can_delete_extra = False)

class MethodForm(forms.ModelForm):
    class Meta:
        model = MethodStep
        exclude = ['recipe',]

MethodFormSet = inlineformset_factory(
    RecipeCard, MethodStep, form = MethodForm, can_delete_extra = False)
