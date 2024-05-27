
from django.urls import path
from .views import MealOffView, MealOffSuccessView

urlpatterns = [
    
    path('meal_off/', MealOffView.as_view(), name='meal_off'),
    path('meal_off_success/', MealOffSuccessView.as_view(), name='meal_off_success'),
]
