from django.shortcuts import render, redirect
from django.utils import timezone

from django.views import View
from django.views.generic import TemplateView, CreateView

from django.urls import reverse_lazy, reverse
from .forms import NewUserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Subscription, Order
from .forms import MealOffForm, OrderForm

from django.db.models import Count


class HomeView(TemplateView):

    template_name = 'base.html'


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'foodbear_app/success_page.html'
    login_url = reverse_lazy('login')


class MealOffView(LoginRequiredMixin, View):

    form_class = MealOffForm
    template_name = 'foodbear_app/meal_off.html'
    login_url = reverse_lazy('login')

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

# Feature#2: Reduce Balance


class OrderMealView(LoginRequiredMixin, View):

    template_name = 'foodbear_app/order_meal.html'
    form_class = OrderForm
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            subscription = Subscription.objects.get(user=request.user)
            if not self.subscription:
                return render(request, self.template_name, {'error_message': 'You do not have a subscription.'})

            cost_per_meal = subscription.total_cost / \
                (subscription.plan_days * 2)

            meal_type = form.cleaned_data['meal_type']

            if cost_per_meal >= subscription.balance:

                if meal_type == 'lunch' and not subscription.lunch_off:

                    subscription.balance -= cost_per_meal
                    subscription.save()

                    return render(request, 'foodbear_app/success_page.html', {'messages': 'Order Successful', 'new_balance': subscription.balance})

                elif meal_type == 'dinner' and not subscription.dinner_off:
                    subscription.balance -= cost_per_meal
                    subscription.save()

                    return render(request, 'foodbear_app/success_page.html', {'messages': 'Order Successful', 'new_balance': subscription.balance})

                elif subscription.dinner_off or subscription.lunch_off:
                    return render(request, 'foodbear_app/success_page.html', {'error_message': 'Meal turned off already.'})

            else:
                return render(request, 'foodbear_app/success_page.html', {'error_message': 'You do not have enough balance.'})

            form.save(commit=False)
            form.user = request.user
            form.category = subscription.category
            print(subscription.category)
            form.save()

        return render(request, self.template_name, {"form": form})


class DailyOrdersView(LoginRequiredMixin, View):

    template_name = 'foodbear_app/daily_orders.html'
    login_url = reverse_lazy()
    def get(self, request, *args, **kwargs):


        orders = Order.objects.all()

        lunch = orders.filter(meal_type='lunch').values_list(
            'category').annotate(count=Count('category'))

        dinner = orders.filter(meal_type='dinner').values_list(
            'category').annotate(count=Count('category'))

        stats = {'lunch':
                 {'basic': 0, 'premium': 0},
                 'dinner':
                 {'basic': 0, 'premium': 0}
                }

        for l_stat in lunch:

            stats['lunch'][l_stat[0]] = l_stat[1]

        for d_stat in dinner:

            stats['dinner'][d_stat[0]] = d_stat[1]

        return render(request, self.template_name, {'stats': stats})


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = NewUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('success_page')
    success_message = "Registration successful."
