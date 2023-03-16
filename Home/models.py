from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta


class Activity(models.Model):
    """ Activity data. """

    class ActivityType(models.TextChoices):
    # https://evofitness.de/en/magazine/training/welche-sportart-verbrennt-am-meisten-kalorien-wir-l%C3%B6sen-auf
        YOGA = 'YOGA', _('Yoga')
        SWIMMING = 'SWIM', _('Swimming')
        JOGGING = 'JOGG', _('Jogging')
        CYCLING = 'CYCL', _('Cycling')
        SPINNING = 'SPIN', _('Running')
        LIFT_WEIGHT = 'LWGT', _('Lift Weight')
        CROSS_COUNTRY_SKIING = 'CCSK', _('Cross Country Skiing')
        HIGH_INTENSITY_INTERVAL_TRAINING = 'HIIT', _('High-intensity interval training')

    activity = models.CharField(max_length=4, choices=ActivityType.choices)
    duration = models.DurationField()
    calories_burned_per_hour = {
        choice: (400, 425, 650, 525, 700, 425, 600, 900)[i]
        for i, choice in enumerate(ActivityType.choices)
    }

    def get_calories(self):
        """ Associate an average range of calories during an hour for a given activity. """
        return self.calories_burned_per_hour[self.activity] * (self.duration.total_seconds() / 3600)


class Food(models.Model):
    """ Food data. """

    class FoodLabel(models.TextChoices):
        MEAL = 'MEAL', _('Meal')
        INGR = 'INGR', _('Ingredient')
            
    name = models.CharField(max_length=50)
    calories = models.FloatField()
    label = models.CharField(max_length=4, choices=FoodLabel.choices)


class Result(models.Model):
    """ User's daily data. """
    
    date = models.DateField(default=timezone.now)
    sleep = models.FloatField()
    weight = models.FloatField()
    waterIngested = models.FloatField()
    activities = models.ForeignKey(Activity, on_delete=models.CASCADE)
    meals = models.ForeignKey(Food, on_delete=models.CASCADE)


class Account(models.Model):
    """ User's account. """

    class GoalType(models.TextChoices):
        MAINTAIN_WEIGHT = 'M', _('Maintain Weight')
        LOSE_WEIGHT = 'L', _('Lose Weight')
        GAIN_WEIGHT = 'G', _('Gain Weight')
    
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(validators=[MinValueValidator(timezone.now().date() - timedelta(days=365*100))])
    gender = models.CharField(max_length=1, choices=Gender.choices)
    weight = models.FloatField(validators=[MinValueValidator(20.0)])
    goalWeight = models.FloatField(validators=[MinValueValidator(20.0)])
    goalType = models.CharField(max_length=1, choices=GoalType.choices)
    results = models.ForeignKey(Result, on_delete=models.CASCADE)