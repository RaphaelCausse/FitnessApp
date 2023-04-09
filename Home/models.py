from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta, date


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

    def __str__(self) -> str:
        """ Used for admin panel visibility. """
        return self.activity

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

    def __str__(self):
        """ Used for admin panel visibility. """
        return f"{self.label}, {self.name}"


class Result(models.Model):
    """ User's daily results. """
    date = models.DateField(auto_now_add=True)
    sleep = models.TimeField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    waterCups = models.FloatField(default=0)
    steps = models.PositiveSmallIntegerField(default=0)
    activities = models.ForeignKey(Activity, default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    meals = models.ForeignKey(Food, default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)

    def __str__(self):
        """ Used for admin panel visibility. """
        return f"{self.date} of {Account.objects.get(result=self).user.username}"


class Account(models.Model):
    """ User's account. """
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'

    class LifeStyle(models.TextChoices):
        ACTIVE_NONE = 'ANO', _('No activity')
        ACTIVE_LOW = 'ALOW', _('Low activity')
        ACTIVE_MED = 'AMED', _('Medium activity')
        ACTIVE_INT = 'AINT', _('Intense activity')
        ACTIVE_PRO = 'APRO', _('Professional activity')

    class GoalType(models.TextChoices):
        GAIN_WEIGHT = 'G', _('Gain Weight')
        MAINTAIN_WEIGHT = 'M', _('Maintain Weight')
        LOSE_WEIGHT = 'L', _('Lose Weight')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(validators=[MinValueValidator(
        timezone.now().date() - timedelta(days=365*100))])
    gender = models.CharField(max_length=1, choices=Gender.choices)
    weight = models.FloatField(validators=[MinValueValidator(20.0)])
    height = models.FloatField(validators=[MinValueValidator(20.0)])
    lifestyle = models.CharField(max_length=4, choices=LifeStyle.choices)
    goalType = models.CharField(max_length=1, choices=GoalType.choices)
    goalWeight = models.FloatField(validators=[MinValueValidator(20.0)])
    goalCalories = models.PositiveSmallIntegerField(blank=True, null=True)
    results = models.ForeignKey(Result, default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)

    def __str__(self):
        """ Used for admin panel visibility. """
        return self.user.username

    def get_age(self):
        """ Age of account user. """
        today = date.today()
        age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        return age
    
    def set_goal_calories(self):
        """ Compute and set goal calories value for account profile. """
        age = self.get_age()
        baseMetabolism = (10*float(self.weight)) + (6.25*float(self.height)) - (5*float(age))
        if self.gender == "M":
            baseMetabolism += 5.0
        elif self.gender == "F":
            baseMetabolism -= 161.0
        activity = { 'ANO': 1.2, 'ALOW': 1.375, 'AMED': 1.55, 'AINT': 1.725, 'APRO': 1.9 }
        self.goalCalories = round(baseMetabolism * activity.get(self.lifestyle, 1.2)) 


class SocialPost(models.Model):
    """ Social posts. """
    class Meta:
        ordering = ['-created']

    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    likes = models.PositiveSmallIntegerField(default=0)
    dislikes = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """ Used for admin panel visibility. """
        return f"{self.created} from {self.author.user.username}"