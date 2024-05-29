from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Subscription(models.Model):

    PLAN_CHOICES = (
        (3, '3 Days'),
        (7, '7 Days'),
        (15, '15 Days'),
        (30, '30 Days'),
    )

    CATEGORY_CHOICES = (

        ('basic', 'Basic'),
        ('premium', 'Premium'),

    )

    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )

    Category_Dictionary = {
        'basic': 1.5,
        'premium': 2.75,
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES)
    plan_days = models.IntegerField(choices=PLAN_CHOICES)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    lunch_off = models.BooleanField(default=False)
    dinner_off = models.BooleanField(default=False)
    total_cost = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2 )
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.plan_days} days"

    def save(self, *args, **kwargs):

        if not self:
            self.total_cost = self.plan_days * self.Category_Dictionary[self.category]
        
        super(Subscription, self).save(*args, **kwargs)


class Order(models.Model):

    CATEGORY_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium')
    ]
    
    MEAL_CHOICES = [
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES)
    meal_type = models.CharField(max_length=6, choices=MEAL_CHOICES)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.meal_type}"
