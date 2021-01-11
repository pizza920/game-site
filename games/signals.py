from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_out
from .models import Profile, User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        profile = instance.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(user_logged_out)
def create_or_update_user_profile(sender, request, user, **kwargs):
    if user and user.profile and user.profile.online:
        user.profile.online = False
        user.profile.save()