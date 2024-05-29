import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from foodbear_app.models import Subscription, Order
from datetime import datetime, timedelta
from django.utils import timezone
from operator import *
import uuid
fake = Faker()
operators = [add, sub, mul]

class Command(BaseCommand):

    help = 'Generate fake data for User, Subscription, and Order models'

    def handle(self, *args, **kwargs):
        # self.create_users()
        # self.create_subscriptions()
        self.create_orders()

    def create_users(self):
        # Create users if they do not already exist
        for i in range(100):
            User.objects.get_or_create(
                username=f'user_{i+1}',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=f'{fake.first_name()}.{fake.last_name()}@{fake.free_email_domain()}',
                password='password'
            )
        
        self.stdout.write(self.style.SUCCESS('Users created'))

    def create_subscriptions(self):

        users = User.objects.all()

        categories = ['basic', 'premium']
        plan_days_options = [3, 7, 15, 30]

        for user in users:
                
            category = random.choice(categories)
            plan_days = random.choice(plan_days_options)
            start_date = timezone.now()
            end_date = start_date + timedelta(days=plan_days)
            total_cost = float(plan_days * Subscription.Category_Dictionary[category])
            balance = float(random.choice(operators)(total_cost, 10))   # You can modify this as per your logic
            status = random.choice([True, False])
            
            Subscription.objects.create(
                user=user,
                category=category,
                plan_days=plan_days,
                start=start_date,
                end=end_date,
                balance=balance,
                total_cost=total_cost,
                status=status
            )

        self.stdout.write(self.style.SUCCESS('Subscriptions created'))

    def create_orders(self):
        users = User.objects.all()

        categories = ['basic', 'premium']
        meal_types = ['lunch', 'dinner']

        for user in users:

            if not user.subscriptions.all()[0].status:
                continue

            for _ in range(2):  # Create 2 orders per user

                category = random.choice(categories)
                meal_type = random.choice(meal_types)

                Order.objects.create(
                    user=user,
                    category=category,
                    meal_type=meal_type,
                )

        self.stdout.write(self.style.SUCCESS('Orders created'))
