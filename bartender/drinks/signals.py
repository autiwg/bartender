from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from bartender.drinks.models import Crate


@receiver(pre_save, sender=Crate)
def set_billed_at(sender, instance, *args, **kwargs):
    try:
        old_instance = Crate.objects.get(id=instance.id)
        if instance.billed is True and old_instance.billed is not True:
            instance.billed_at = timezone.now()
    except Crate.DoesNotExist:
        pass
