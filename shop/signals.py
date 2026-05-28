# shop/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from .models import Laptop, Monitor, Keyboard, CPUModel, GraphicsCard


@receiver(post_save, sender=Laptop)
@receiver(post_save, sender=Monitor)
@receiver(post_save, sender=Keyboard)
@receiver(post_save, sender=CPUModel)
@receiver(post_save, sender=GraphicsCard)
def update_document(sender, instance, **kwargs):
    """به‌روزرسانی خودکار ایندکس هنگام ذخیره محصول"""
    registry.update(instance)


@receiver(post_delete, sender=Laptop)
@receiver(post_delete, sender=Monitor)
@receiver(post_delete, sender=Keyboard)
@receiver(post_delete, sender=CPUModel)
@receiver(post_delete, sender=GraphicsCard)
def delete_document(sender, instance, **kwargs):
    """حذف خودکار از ایندکس هنگام حذف محصول"""
    registry.delete(instance)
