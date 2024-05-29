from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from . models import *

class NewUserForm(UserCreationForm):
	
	email = forms.EmailField(
		required=True,
		label="",
		widget=forms.EmailInput(attrs={
			'class' : 'form-control',
			'placeholder' : 'Email',
			
		})
	)
	password1 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={
			'class' : 'form-control',
			'placeholder' : 'Password',
		}),
		help_text=password_validation.password_validators_help_text_html(),
	)
	password2 = forms.CharField(
		label="",
		widget=forms.PasswordInput(attrs={
			'class' : 'form-control',
			'placeholder' : 'Retype Password',
		})	
	)
	username = forms.CharField(
		label="",
		widget=forms.TextInput(attrs={
			'class' : 'form-control',
			'placeholder' : 'Username'
		})
	)
	
	class Meta:

		model = User
		fields = ("first_name", "last_name", "username", "email", "password1", "password2")
		
		labels = {
			'first_name' : _(''),
			'last_name' : _(''),
		}

		widgets = {
			'first_name' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'First Name',
			}),
			'last_name' : forms.TextInput(attrs={
				'class' : 'form-control',
				'placeholder' : 'Last Name',
			}),
		}


	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


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
