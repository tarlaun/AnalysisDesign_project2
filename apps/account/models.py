from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import IntegerChoices
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class UserType(IntegerChoices):
    DOCTOR = 1,
    PATIENT = 2


# Our Custom User Model
class Account(AbstractUser):
    user_type = models.SmallIntegerField('user_type', choices=UserType.choices, default=UserType.PATIENT)
    phone_regex = RegexValidator(regex=r'^(\+|0)9\d{9,11}$',
                                 message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=False)  # validators should be a list

    def __str__(self):
        return self.username

    @staticmethod
    def get_fields():
        return 'username', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'password'

    @staticmethod
    def get_form_fields():
        return 'username', 'email', 'first_name', 'last_name', 'phone_number'


class Expertise(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# each doctor type account is related to a doctor entry
class Doctor(models.Model):
    expertise = models.ForeignKey(Expertise, on_delete=models.PROTECT)
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    not_processed_income = models.IntegerField(default=0)

    @staticmethod
    def get_fields():
        return 'user', 'expertise'

    def __str__(self):
        return self.user.__str__()


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.PROTECT, null=False)
    doctor = models.ForeignKey(Doctor, null=True, blank=True, on_delete=models.PROTECT)
    expertise = models.ForeignKey(Expertise, on_delete=models.PROTECT)
    address = models.TextField()
    details = models.TextField()
    score = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    comment = models.TextField()

    # NEW: added this field to show if doctor has accepted request or not
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.__str__()} {self.doctor.__str__()} {self.expertise.__str__()}'
