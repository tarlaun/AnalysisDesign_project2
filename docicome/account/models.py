from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import IntegerChoices

# Create your models here.

class UserType(IntegerChoices):
    DOCTOR = 1,
    PATIENT = 2
  
class Account(AbstractUser):
    user_type = models.SmallIntegerField('user_type', choices=UserType.choices, default=UserType.PATIENT)
    # add additional fields in here


    def __str__(self):
        return self.username

    @staticmethod
    def get_fields():
        return 'username', 'email', 'first_name', 'last_name', 'user_type'

# Create your models here.

class Doctor(models.Model):
    specialty = models.TextField()
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    
    @staticmethod
    def get_fields():
        return 'user', 'specialty'
