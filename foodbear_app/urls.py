
from django.urls import path
from .views import MealOffView, SuccessView, OrderMealView, HomeView
from .admin_views import DailyOrdersView

urlpatterns = [
    
    path('', HomeView.as_view(), name='home'),
    path('meal_off/', MealOffView.as_view(), name='meal_off'),
    path('meal_off_success/', SuccessView.as_view(), name='success_page'),
    path('order_meal/', OrderMealView.as_view(), name='order_meal'),
    path('daily_orders/', DailyOrdersView.as_view(), name='daily_orders'),

]
