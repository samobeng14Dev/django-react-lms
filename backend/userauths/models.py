from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create a custom your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    # if not to check if the field is empty or not

    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split('@')
        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='user_folder',
                             default='default.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.email)

    # if not to check if the field is empty or not
    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super().save(*args, **kwargs)
# corresponding profile when user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# if instance is updated, the related Profile instance is also saved.
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()     
# connect signals to user model    
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
