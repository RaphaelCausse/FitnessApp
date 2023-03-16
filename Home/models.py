from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import date, timedelta
from django.core.validators import MinValueValidator


class Activity(models.Model):
    # https://evofitness.de/en/magazine/training/welche-sportart-verbrennt-am-meisten-kalorien-wir-l%C3%B6sen-auf
    class ActivityType(models.TextChoices):
        YOGA = 'YOGA', _('Yoga')
        SWIMMING = 'SWIM', _('Swimming')
        JOGGING = 'JOGG', _('Jogging')
        CYCLING = 'CYCL', _('Cycling')
        SPINNING = 'SPIN', _('Running')
        LIFT_WEIGHT = 'LWGT', _('Lift Weight')
        CROSS_COUNTRY_SKIING = 'CCSK', _('Cross Country Skiing')
        HIGH_INTENSITY_INTERVAL_TRAINING = 'HIIT', _('High-intensity interval training')

    activity = models.CharField(
        max_length=4,
        choices=ActivityType.choices,
    )
    duration = models.DurationField(default=3600)  # model.DoubleField()
    calories_burned_per_hour = {
        choice: (400, 425, 650, 525, 700, 425, 600, 900)[i]
        for i, choice in enumerate(ActivityType.choices)
    }

    def get_calories(self):
        # associate an average range of calories during an hour for a given activity
        return self.calories_burned_per_hour[self.activity] * (self.duration.total_seconds() / 3600)


class Product(models.Model):
    class ProductLabel(models.TextChoices):
        MEAL = 'MEAL', _('Meal')
        INGR = 'INGR', _('Ingredient')
            
    name = models.CharField(max_length=50)
    calories = models.FloatField()
    label = models.CharField(max_length=4, choices=ProductLabel.choices)


class Result(models.Model):
    sleep = models.FloatField(default=7)
    weight = models.FloatField()
    waterIngested = models.FloatField()
    activities = models.ForeignKey(Activity, on_delete=models.CASCADE)
    meals = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)


class Account(models.Model):
    class GoalType(models.TextChoices):
        MAINTAIN_WEIGHT = 'M', _('Maintain Weight')
        LOSE_WEIGHT = 'L', _('Lose Weight')
        GAIN_WEIGHT = 'G', _('Gain Weight')
    
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    results = models.ForeignKey(Result, on_delete=models.CASCADE)
    weight = models.FloatField(validators=[MinValueValidator(20.0)])
    goalWeight = models.FloatField(default=None, validators=[MinValueValidator(20.0)])
    goalType = models.CharField(max_length=1, default='L', choices=GoalType.choices)
    birthdate = models.DateField(default=None, validators=[MinValueValidator(timezone.now().date() - timedelta(days=365*100))])
    gender = models.CharField(max_length=1, choices=Gender.choices)


