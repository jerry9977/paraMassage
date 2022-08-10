from django.db.models.signals import post_save
from django.dispatch import receiver
import main.models as m
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=m.RemedialMedicalHistory)
def historyPostSave(sender, instance, **kwargs):

    remedial_client_info = instance.remedial_client_info

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_consumer',
        {
            'type': 'send_data',
            'action_type': 'add_remedial_client',
            'payload':{
                'id': remedial_client_info.id,
                'first_name':remedial_client_info.client.first_name,
                'last_name':remedial_client_info.client.last_name,
                'health_insurance_number':str(remedial_client_info.health_insurance_number),
                'suffix': str(remedial_client_info.suffix)
            }
            
        }
    )



@receiver(post_save, sender=m.RemedialMedicalHistory)
def historyPostSave(sender, instance, **kwargs):

    remedial_client_info = instance.remedial_client_info

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'dashboard_consumer',
        {
            'type': 'send_data',
            'action_type': 'add_remedial_client',
            'payload':{
                'id': remedial_client_info.id,
                'first_name':remedial_client_info.client.first_name,
                'last_name':remedial_client_info.client.last_name,
                'health_insurance_number':str(remedial_client_info.health_insurance_number),
                'suffix': str(remedial_client_info.suffix)
            }
            
        }
    )