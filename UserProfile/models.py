from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, mobile, otp, **extra_fields):
        if not email and not mobile:
            raise ValueError('The Email or Mobile number must be set')
        user = self.model(email=email, mobile=mobile, otp=otp, **extra_fields)
        user.set_password(otp)  # For simplicity, use OTP as password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, otp, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, mobile, otp, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Change this if you want to use mobile as username
    REQUIRED_FIELDS = ['mobile', 'otp']

    objects = UserManager()

    def __str__(self):
        return str(self.email)