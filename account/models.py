from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import random_number

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        return self._create(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):

        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        return self._create(email, password, **kwargs)


class Region(models.Model):
    name = models.CharField(max_length=55, unique=True)

    def __str__(self) -> str:
        return self.name

class School(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.code = random_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} -> ({self.region.name}), code->({self.code})"
    
    def get_director(self):
        director = User.objects.filter(school=self, role='director').first()
        return f"{director.email}" if director else "No director"


class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('director', 'Director'),
    )

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    username = None
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=False)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=False, related_name='user')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()