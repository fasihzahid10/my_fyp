from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import TradingCenter.models as m

@receiver(post_save, sender=User)
def save_custmer(sender, instance, created, **kwarg):
    if created:
        ins = m.finantial_account.objects.create()
        m.customer.objects.create(user = instance,customers_account = ins)