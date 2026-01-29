from django.db.models.signals import post_save
from django.dispatch import receiver
from data_manager.models import DataSource
from .utils import generate_summary

@receiver(post_save, sender=DataSource)
def auto_generate_summary(sender, instance, created, **kwargs):
    if created:
        generate_summary(instance)