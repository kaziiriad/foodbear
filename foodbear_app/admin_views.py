from django.shortcuts import render
from django.views import View

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import Order
from django.db.models import Count

@method_decorator(staff_member_required, name='dispatch')
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
