from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, email, password, name, **fields):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, name, **fields):
        fields.setdefault('is_active', False)
        fields.setdefault('is_staff', False)
        return self._create(email, password, name, **fields)

    def create_superuser(self, email, password, name, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', True)
        return self._create(email, password, name, **fields)


class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True, verbose_name='activation_code')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(20)
        self.activation_code = code
        self.save()
        return code

    def send_activation_code(self):
        activation_link = f'http://localhost:8000/account/activation/' \
                          f'{self.activation_code}'
        send_mail(subject='Activation',
                  message=activation_link,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[self.email],
                  fail_silently=False)
