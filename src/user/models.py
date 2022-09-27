import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

class RaceChoiceField(models.Model):
    description = models.CharField(max_length=64)
 
    def __str__(self):
        return self.description


class SexChoiceField(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description

class Company(models.Model):
    description = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.description

class User(AbstractUser, PermissionsMixin):
    class Roles(models.IntegerChoices):
        CITIZEN = 0, "CITIZEN"
        SECURITY = 1, "SECURITY"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.SmallIntegerField(choices=Roles.choices, default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'

    def user_role(self):
        return f'{self.role.description}'

class Citizen(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=256, blank=True, null=True)
    sex = models.ForeignKey(SexChoiceField, on_delete=models.PROTECT, blank=True, null=True)
    race = models.ForeignKey(RaceChoiceField, on_delete=models.PROTECT, blank=True, null=True)
    contact_number = PhoneNumberField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.user.first_name

class Security(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sex = models.ForeignKey(SexChoiceField, on_delete=models.PROTECT, blank=True, null=True)
    race = models.ForeignKey(RaceChoiceField, on_delete=models.PROTECT, blank=True, null=True)
    contact_number = PhoneNumberField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=256, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name