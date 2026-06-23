from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default-avatar.png')
    dob = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class SocialAccount(models.Model):
    """Stores OAuth tokens for connected social platforms"""
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    access_token = models.TextField()
    account_id = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    connected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'platform')

    def __str__(self):
        return f"{self.user.username} - {self.platform} (@{self.username})"


class Post(models.Model):
    """Stores posts created by users"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    media_url = models.URLField(blank=True)       # public URL after upload
    media_file = models.FileField(upload_to='posts/', blank=True, null=True)
    platforms = models.JSONField(default=list)     # ['instagram', 'facebook']
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.created_at.strftime('%Y-%m-%d')}"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('YouTube', 'YouTube'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.platform}"

    class Meta:
        unique_together = ('user', 'platform')