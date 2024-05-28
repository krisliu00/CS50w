from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    username = models.CharField(max_length=64, unique=True)
    custom_name = models.CharField(max_length=64)

    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=64, unique=True)

CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )

class UserProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followings',)
    follower = models.ManyToManyField('self', symmetrical=False, related_name='followers', )

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)