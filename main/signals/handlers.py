import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import main.models as m
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer





@receiver(post_save, sender=m.DetailClientInfo)
def client_post_save(sender, **kwargs):
    instance = kwargs.get("instance", None)
    created = kwargs.get("created", None)
    if created:
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'dashboard_consumer',
                {
                    'type': 'send_data',
                    'action_type': "add_remedial_client",
                    'payload':{
                        'id': instance.id,
                        'client_id': instance.client.id,
                        'first_name':instance.client.first_name,
                        'last_name':instance.client.last_name,
                        'health_insurance_number': str(instance.health_insurance_number),
                        'suffix': str(instance.suffix),
                        'date_created': datetime.datetime.strftime(instance.date_created, "%d %b %Y %H:%M"),
                        
                    }
                    
                }
            )
        except Exception as e:
            print(e,flush=True)
    


    


@receiver(post_save, sender=m.ClientMedicalHistory)
def history_post_save(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance:
        detail_client_info = instance.detail_client_info
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        action_type = 'add_remedial_history'

        if instance.date_created < today:
            action_type = 'add_missing_receipt'

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'dashboard_consumer',
            {
                'type': 'send_data',
                'action_type': action_type,
                'payload':{
                    'id': instance.id,
                    'client_id': detail_client_info.client.id,
                    'first_name':detail_client_info.client.first_name,
                    'last_name':detail_client_info.client.last_name,
                    'date_created': datetime.datetime.strftime(instance.date_created, "%d %b %Y %H:%M"),
                    'receipt_image': instance.receipt_image.url if instance.receipt_image else ""
                }
                
            }
        )
