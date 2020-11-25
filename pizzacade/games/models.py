from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


TEMPERAMENT_CHOICES = (
    ('Shy', 'Shy'),
    ('Outgoing', 'Outgoing'),
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(18)])
    temperament = models.CharField(null=True, blank=True, choices=TEMPERAMENT_CHOICES, max_length=24)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        profile = instance.profile
    except ObjectDoesNotExist:
        profile = Profile.objects.create(user=instance)
        profile.save()
