from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    '''

    Custom User model representing a user in the User Management System
    Inherits from the built-in AbstractUser model provided by Django.
    Include additional fields:

    Fields:
    - email (EmailField) : The user email address
    - phone_Number (IntegerField) : The user phone number
    -street (CharField) : the user street address
    - zip_code (CharFields) : the user zip code
    - city (CharField) : the user city
    - state (CharField) : the user state
    - country (CharField) : the user country
    - date_of_birth (DateField) : the user DOB

    '''
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_Number = models.IntegerField(unique=True, null=False)
    street = models.CharField(max_length=20, null=False)
    zip_code = models.CharField(null=False, max_length=6)
    city = models.CharField(max_length=10, null=False)
    state = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=10, null=False)
    date_of_birth = models.DateField(blank=False)
