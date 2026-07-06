import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, phone_number=None, password=None) -> "User":
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
        user.is_active = True
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, first_name, last_name, phone_number=None, password=None) -> "User":
        return self._create_user(email, first_name, last_name, phone_number, password)

    def create_superuser(self, email, first_name, last_name, phone_number=None, password=None) -> "User":
        user = self._create_user(email, first_name, last_name, phone_number, password)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
    def __str__(self):
        return self.email