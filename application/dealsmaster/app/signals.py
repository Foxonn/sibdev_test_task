from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Deal, Gem, Person


@receiver(post_save, sender=Deal)
@receiver(post_save, sender=Gem)
@receiver(post_save, sender=Person)
@receiver(post_delete, sender=Deal)
@receiver(post_delete, sender=Gem)
@receiver(post_delete, sender=Person)
def clear_cache(sender, instance, **kwargs):
    cache.clear()
