import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from foodbear_app.models import Subscription, Order
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    
    help = 'Generate fake data for User, Subscription, and Order models'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        for _ in range(50):
            User.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password='password123'
            )

        self.stdout.write(self.style.SUCCESS('Successfully created users.'))

        # Create Subscriptions
        users = User.objects.all()

        plan_days_choices = [3, 7, 15, 30]
        category_choices = ['basic', 'premium']

        for user in users:  
            plan_days = random.choice(plan_days_choices)
            category = random.choice(category_choices)
            Subscription.objects.create(
                user=user,
                plan_days=plan_days,
                category=category,
                start=fake.date_this_year(),
                end=fake.date_this_year(),
                balance=plan_days * category * 10  # Assuming a base price of 10 per day
            )

        self.stdout.write(self.style.SUCCESS('Successfully created subscriptions.'))

        # Create Orders
        meal_choices = ['lunch', 'dinner']
        for _ in range(100):
            user = random.choice(users)
            category = random.choice(category_choices)
            meal_type = random.choice(meal_choices)
            Order.objects.create(
                user=user,
                category=category,
                meal_type=meal_type,
                order_date=fake.date_this_year()
            )

        self.stdout.write(self.style.SUCCESS('Successfully created orders.'))
