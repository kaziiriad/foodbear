from django.shortcuts import render, redirect
from django.utils import timezone

from django.views import View
from django.views.generic import TemplateView

from .models import Subscription, Order
from .forms import MealOffForm, OrderForm

from django.db.models import Count


class HomeView(TemplateView):

    template_name = 'base.html'

class SuccessView(TemplateView):
    template_name = 'foodbear_app/success_page.html'


class MealOffView(View):

    form_class = MealOffForm
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
            return redirect('success_page')

        return render(request, self.template_name, {"form": form})

## Feature#2: Reduce Balance
class OrderMealView(View):

    template_name = 'foodbear_app/order_meal.html'
    form_class = OrderForm


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        
        form = self.form_class(request.POST)

        if form.is_valid():

            subscription = Subscription.objects.get(user=request.user)
            if not self.subscription:
                return render(request, self.template_name, {'error_message': 'You do not have a subscription.'})

            
            cost_per_meal = subscription.total_cost / (subscription.plan_days * 2)
            meal_type = form.cleaned_data['meal_type']

            if cost_per_meal >= subscription.balance:

                if meal_type == 'lunch' and not subscription.lunch_off:

                    subscription.balance -= cost_per_meal
                    subscription.save()

                    return render(request, 'foodbear_app/success_page.html', {'message': 'Order Successful', 'new_balance': subscription.balance})
                else:
                    return render(request, 'foodbear_app/success_page.html', {'error_message': 'Meal turned off already.'})
                
                if meal_type == 'dinner' and not subscription.dinner_off:
                    subscription.balance -= cost_per_meal
                    subscription.save()

                    return render(request, 'foodbear_app/success_page.html', {'message': 'Order Successful', 'new_balance': subscription.balance})
                else:
                    return render(request, 'foodbear_app/success_page.html', {'error_message': 'Meal turned off already.'})
            else:
                return render(request, 'foodbear_app/success_page.html', {'error_message': 'You do not have enough balance.'})


            form.save(commit=False)
            form.user = request.user
            form.category = subscription.category
            print(subscription.category)            
            form.save()
        
        return render(request, self.template_name, {"form": form})


class DailyOrdersView(View):

    template_name = 'foodbear_app/daily_orders.html'
    def get(self, request, *args, **kwargs):

        today = timezone.now().date()
        subsciption = Subscription.objects.all()
        orders = Order.objects.filter(order_date=today).values('category', 'meal_type').annotate(count=Count('id'))
        
        stats = {'lunch': 
                    {'basic': 0, 'premium': 0}, 
                'dinner': 
                    {'basic': 0, 'premium': 0}}
        for order in orders:
            stats[order['meal_type']][order['category']] = order['count']
            print(order['count'])

        print(stats)
        return render(request, self.template_name, {'data': stats})
    

