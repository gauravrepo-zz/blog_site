from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.
def upload_location(instance, filename):
    file_path = 'accounts/{username}/display.jpg'.format(
        username=str(instance.username), filename=filename
    )
    return file_path

class AccountManager(BaseUserManager):
    # Method to create simple user
    def create_user(self, email, username, first_name, last_name, password=None, **kwargs):
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have a username")

        if not first_name:
            raise ValueError("User must have a first name")

        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create superuser
    def create_superuser(self, email, username, first_name, last_name, password, **kwargs):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# User Authentication model 
class Account(AbstractBaseUser):
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username    = models.CharField(verbose_name="username", max_length=30, unique=True)
    first_name  = models.CharField(verbose_name="first_name", max_length=30)
    last_name   = models.CharField(verbose_name="last_name", max_length=30)
    image       = models.ImageField(upload_to=upload_location, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login  = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active    = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    avatar      = ImageSpecField(source="image", processors=[ResizeToFill(72, 72)], format='JPEG', options={'quality': 60})
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Signal to delete the image assosciated with the user
@receiver(post_delete, sender= Account)
def delete_profile_image(sender, instance, **kwargs):
    instance.image.delete(False)