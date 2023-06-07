from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''

    Custom User model representing a user in the User Management System
    Inherits from the built-in AbstractUser model provided by Django.
    Include additional fields:

    Fields:
    - email (EmailField) : The user email address
    - phone_Number (CharField) : The user phone number
    -street (CharField) : the user street address
    - zip_code (IntegerField) : the user zip code
    - city (CharField) : the user city
    - state (CharField) : the user state
    - country (CharField) : the user country
    - date_of_birth (DateField) : the user DOB
    '''
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_Number = models.CharField(max_length=20, unique=True, blank=False, validators=[MinLengthValidator(10)])
    street = models.CharField(max_length=20, null=False, blank=False)
    zip_code = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(6)])
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    date_of_birth = models.DateField(blank=False, null=False)

    user_permissions = None
    groups = None
