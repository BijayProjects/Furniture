# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, PaidOrder


@receiver(post_save, sender=Order)
def move_to_completed(sender, instance, created, **kwargs):
    if not created and instance.status == 'Completed':
        # Check if already in OrderComplete to avoid duplicates
        if not PaidOrder.objects.filter(
            customer_name=instance.customer_name,
            address =instance.address,
            product=instance.product_name,
            quantity=instance.quantity,
            price=instance.total_price,
        ).exists():
            PaidOrder.objects.create(
                customer_name=instance.customer_name,
                address =instance.address,
                product=instance.product_name,
                quantity=instance.quantity,
                price=instance.total_price,
            )
