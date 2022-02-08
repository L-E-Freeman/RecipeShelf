from django import forms
from .models import Ingredient, MethodStep, RecipeCard
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

# Forms created using models. Formsets created using the forms which allow 
# the same form to be repeated many times on a single page.


class RecipeForm(forms.ModelForm):
    class Meta:
        model = RecipeCard
        # User field isn't to be entered in to the form, so we exclude it and 
        # can associate a user with the post in views.
        exclude = ['user']

    def clean(self):
        """
        Overrides clean() method with custom validation for 
        recipe timings.
        """
        cleaned_data = super().clean()
        ath = cleaned_data.get("active_time_hours")
        atm = cleaned_data.get("active_time_minutes")
        tth = cleaned_data.get("total_time_hours")
        ttm = cleaned_data.get("total_time_minutes")

        active_counter = 0
        total_counter = 0

        # Increment counters if form field is zero.
        if not ath > 0:
            active_counter += 1
        if not atm > 0:
            active_counter += 1
        if not tth > 0:
            total_counter += 1
        if not ttm > 0:
            total_counter += 1

        # Total time fields cannot both be zero, and total recipe 
        # time cannot be zero.
        if total_counter == 2: 
            raise ValidationError("Total time cannot be zero.")
        if active_counter + total_counter == 4:
            raise ValidationError("Total recipe time cannot be zero.") 
        if (ath + atm) > (tth + ttm):
            raise ValidationError(
                "Active time cannot be greater than total time")

        return None


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
    can_delete = False, 
    extra=2,
    max_num=15)

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
    can_delete= False,
    max_num=3)

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class':'validate', 
        'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password'}))