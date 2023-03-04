from django.db import models
from django.utils.translation import gettext_lazy as _


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
    duration = models.DurationField(default=3600) # model.DoubleField()
    calories_burned_per_hour = {
        choice : (400, 425, 650, 525, 700, 425, 600, 900)[i]
            for i, choice in enumerate(ActivityType.choices)
    }


    def get_calories(self):
        # associate an average range of calories during an hour for a given activity
        return self.calories_burned_per_hour[self.activity] * (self.duration.total_seconds() / 3600)

 
class Meal (models.Model):
    name = models.CharField(max_length = 50)
    quantity = models.IntegerField(default = 100)
    calories = models.FloatField()
    
    
class Day(models.Model):
    sleep = models.FloatField(default = 7)
    weight = models.FloatField()
    waterIngested = models.FloatField()
    activities = models.ForeignKey(Activity, on_delete = models.CASCADE)
    meals = models.ForeignKey(Meal, on_delete = models.CASCADE)

class Month(models.Model):
    nbDays = models.IntegerField(default = 1)
    days = models.ForeignKey(Day, on_delete = models.CASCADE)

class Year(models.Model):
    nbMonths = models.IntegerField(default = 1)
    months = models.ForeignKey(Month, on_delete = models.CASCADE)


class Person(models.Model):
    
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    gender = models.CharField(
        max_length=1,
        choices = Gender.choices,
    )

    surname = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    days = models.ForeignKey(Day, on_delete = models.CASCADE)
