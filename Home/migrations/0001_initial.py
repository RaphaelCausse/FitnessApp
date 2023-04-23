# Generated by Django 4.1.7 on 2023-04-23 13:16

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(1923, 5, 18))])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(20.0)])),
                ('height', models.FloatField(validators=[django.core.validators.MinValueValidator(20.0)])),
                ('lifestyle', models.CharField(choices=[('ANO', 'No activity'), ('ALOW', 'Low activity'), ('AMED', 'Medium activity'), ('AINT', 'Intense activity'), ('APRO', 'Professional activity')], max_length=4)),
                ('goalType', models.CharField(choices=[('G', 'Gain Weight'), ('M', 'Maintain Weight'), ('L', 'Lose Weight')], max_length=1)),
                ('goalWeight', models.FloatField(validators=[django.core.validators.MinValueValidator(20.0)])),
                ('goalCalories', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SocialPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('likes', models.PositiveSmallIntegerField(default=0)),
                ('dislikes', models.PositiveSmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Home.account')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('sleep', models.TimeField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('waterCups', models.FloatField(default=0)),
                ('steps', models.PositiveSmallIntegerField(default=0)),
                ('owner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Home.account')),
            ],
        ),
        migrations.CreateModel(
            name='LikedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.account')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.socialpost')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('calories', models.FloatField()),
                ('label', models.CharField(choices=[('MEAL', 'Meal'), ('INGR', 'Ingredient')], max_length=4)),
                ('result', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Home.result')),
            ],
        ),
        migrations.CreateModel(
            name='DislikedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disliker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.account')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.socialpost')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(choices=[('YOGA', 'Yoga'), ('SWIM', 'Swimming'), ('JOGG', 'Jogging'), ('CYCL', 'Cycling'), ('SPIN', 'Running'), ('LWGT', 'Lift Weight'), ('CCSK', 'Cross Country Skiing'), ('HIIT', 'High-intensity interval training')], max_length=4)),
                ('duration', models.DurationField()),
                ('result', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Home.result')),
            ],
        ),
    ]
