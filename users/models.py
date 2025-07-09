from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите аватар")
    country = CountryField(verbose_name="Страна", blank=True, null=True, help_text="Введите страну")

    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Token")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self):
        return self.email

