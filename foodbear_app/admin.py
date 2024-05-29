from django.contrib import admin
from . models import Subscription, Order
from django.urls import path
from .admin_views import DailyOrdersView  # Import your class-based view

class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('daily-orders/', self.admin_view(DailyOrdersView.as_view()), name='daily-orders'),
        ]
        return custom_urls + urls

admin_site = MyAdminSite(name='myadmin')

# Register your models here.
admin.site.register(Subscription)
admin.site.register(Order)

admin.site = admin_site
admin.autodiscover()
