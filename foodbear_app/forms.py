from django.forms import forms
from . models import *

class MealOffForm(forms.Form):

    MEAL_CHOICES = (
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('both', 'Both'),
    )
    meal_type = forms.ChoiceField(choices=MEAL_CHOICES)

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("meal_type",)


# class SubscriptionForm(forms.ModelForm):
    
#     class Meta:
#         model = Subscription
#         exclude = ('user', 'start', 'end', 'lunch_off', 'dinner_off', 'status', 'updated')
