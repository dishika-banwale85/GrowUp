from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only create profile if it does NOT exist already
        Profile.objects.get_or_create(user=instance)
    else:
        # Update profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.save()