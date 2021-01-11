from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.signals import user_logged_out


TEMPERAMENT_CHOICES = (
    ('Boring', 'Boring'),
    ('Quiet', 'Quiet'),
    ('Loud', 'Loud'),
)

INTELLIGENCE_CHOICES = (
    ('Intellectual', 'Intellectual'),
    ('Regular', 'Regular'),
    ('Not at All', 'Not at All'),
)

EDUCATION_CHOICES = (
    ('Educated', 'Educated'),
    ('Regular', 'Regular'),
    ('Under Educated', 'Under Educated'),
)

PERSONALITY_TYPE_CHOICES = (
    ('Type A', 'Type A'),
    ('Type B', 'Type B'),
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(18)])
    temperament = models.CharField(null=True, blank=True, choices=TEMPERAMENT_CHOICES, max_length=24)
    intelligence = models.CharField(null=True, blank=True, choices=INTELLIGENCE_CHOICES, max_length=24)
    personality_type = models.CharField(null=True, blank=True, choices=PERSONALITY_TYPE_CHOICES, max_length=24)
    education = models.CharField(null=True, blank=True, choices=EDUCATION_CHOICES, max_length=24)
    temperament_preference = models.CharField(null=True, blank=True, choices=TEMPERAMENT_CHOICES, max_length=24)
    intelligence_preference = models.CharField(null=True, blank=True, choices=INTELLIGENCE_CHOICES, max_length=24)
    personality_type_preference = models.CharField(null=True, blank=True, choices=PERSONALITY_TYPE_CHOICES, max_length=24)
    education_preference = models.CharField(null=True, blank=True, choices=EDUCATION_CHOICES, max_length=24)
    friends = models.ManyToManyField(to=User, related_name='profile_friends', blank=True)
    online = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def as_json(self):
        picture = None
        if self.picture:
            picture = self.picture.url
        return {
            "id": self.user.id,
            "username": self.user.username,
            "temperament": self.temperament,
            "intelligence": self.intelligence,
            "personality_type": self.personality_type,
            "education": self.education,
            "picture": picture
        }

    def preferences_as_json(self):
        return {
            "temperament": self.temperament_preference,
            "intelligence": self.intelligence_preference,
            "personality_type": self.personality_type_preference,
            "education": self.education_preference,
        }

    def __str__(self):
        return f'Profile for {self.user.username}'


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
