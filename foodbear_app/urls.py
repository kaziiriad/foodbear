
from django.urls import path
from .views import MealOffView, MealOffSuccessView, OrderMealView, DailyOrdersView


urlpatterns = [
    
    path('meal_off/', MealOffView.as_view(), name='meal_off'),
    path('meal_off_success/', MealOffSuccessView.as_view(), name='meal_off_success'),
    path('order_meal/', OrderMealView.as_view(), name='order_meal'),
    path('daily_orders/', DailyOrdersView.as_view(), name='daily_orders'),

]
