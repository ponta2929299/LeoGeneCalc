from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from .models import Morph  

@receiver(pre_save, sender=Morph)
def update_end_instance_id(sender, instance, **kwargs):
    # "end"インスタンスのIDを最大に設定
    if instance.morph_name == "end":
        # 他のインスタンスのIDを確認
        max_id = Morph.objects.all().aggregate(models.Max('id'))['id__max']
        # 最大IDを更新
        instance.id = max_id + 1 if max_id else 1
