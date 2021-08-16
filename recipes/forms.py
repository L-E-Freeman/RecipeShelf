from django import forms
from .models import Ingredient, MethodStep, RecipeCard
from django.forms import inlineformset_factory

# Forms created using models. Formsets created using the forms which allow 
# the same form to be repeated many times on a single page.

class RecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeCard
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['recipe',]

# max_num stops extra forms showing up when user is editing the recipe.
IngredientFormSet = inlineformset_factory(
    RecipeCard, 
    Ingredient, 
    form = IngredientForm, 
    can_delete_extra = False, 
    max_num=3)

class MethodForm(forms.ModelForm):
    class Meta:
        model = MethodStep
        exclude = ['recipe',]

# max_num stops extra forms showing up when user is editing the recipe.
MethodFormSet = inlineformset_factory(
    RecipeCard, 
    MethodStep, 
    form = MethodForm, 
    can_delete_extra = False, 
    max_num=3)
