from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Profile


@receiver(m2m_changed, sender=Profile.user_follow.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_followers = instance.user_follow.count()
    instance.save()


