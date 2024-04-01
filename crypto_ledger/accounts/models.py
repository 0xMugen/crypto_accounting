from django.db import models
from django.contrib.auth.models import AbstractUser

from api.base_models import TimeStampedModel
from utils.custom_functions import full_name




class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

    def confirm_email(self):
        self.email_confirmed = True
        self.save()

class UserProfile(TimeStampedModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def name(self):
        name = full_name(self.user.first_name, self.user.last_name, self.user.email)
        return name





