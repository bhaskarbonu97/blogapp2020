from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, RegexValidator
from django.dispatch import receiver
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True )
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="single", choices=(("single","single"), ("married","married"), ("widow","widow"), ("seprated","seprated"), ("commited","commited")))
    gender = models.CharField(max_length=20, default="female", choices=(("male","male"), ("female","female")))
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(default='profile_pics/default1.jpg', upload_to='profile_pics')
    facebook = models.URLField(max_length=250)
    twitter = models.URLField(max_length=250)
    instagram = models.URLField(max_length=250)
    google_plus = models.URLField(max_length=250)

    def __str__(self):
        return "%s" % self.user

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class FollowUser(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)
