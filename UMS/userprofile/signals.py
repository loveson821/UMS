from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from .models import UserProfile, Ablum
import os

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        userprofile, new = UserProfile.objects.get_or_create(user=instance)


@receiver(post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `User` object is deleted.
    """
    if instance.avator:
        if os.path.isfile(instance.avator.path):
            os.remove(instance.avator.path)

@receiver(pre_save, sender=UserProfile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `User` object is changed.
    """
    if not instance.pk:
        return False

    try:
        old_file = UserProfile.objects.get(pk=instance.pk).avator
    except UserProfile.DoesNotExist:
        return False

    new_file = instance.avator
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)