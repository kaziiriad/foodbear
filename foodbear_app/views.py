from django.shortcuts import render, redirect
from django.utils import timezone

from django.views import View
from django.views.generic import TemplateView

from .models import Subscription
from .forms import SubscriptionForm

class MealOffSuccessView(TemplateView):
    template_name = 'foodbear_app/meal_off_success.html'

class MealOffView(View):

    form_class = SubscriptionForm
    template_name = 'foodbear_app/meal_off.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            meal_type = form.cleaned_data['meal_type']
            current_time = timezone.now()

            subscription = Subscription.objects.filter(user=request.user)

            if 0 <= current_time.hour < 9:
                
                if meal_type == 'lunch': 
                    subscription.lunch_off = True

                elif meal_type == 'both':
                    subscription.lunch_off = True
                    subscription.dinner_off = True

            elif meal_type == 'dinner' and 0 <= current_time.hour < 15:
                subscription.dinner_off = True

            else:
                return render(request, self.template_name, {'form': form, 'error_message': 'You can not order meal at this time.'})

            subscription.save()
            return redirect('meal_off_success')

        return render(request, self.template_name, {"form": form})
    

# class ConsumeMeal(View):        
    
#     subscription = Subscription.objects.filter(user=request.user)

