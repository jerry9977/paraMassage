import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import main.models as m
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer





@receiver(post_save, sender=m.RemedialClientInfo)
def historyPostSave(sender, instance, created, **kwargs):

    if created:
        print("============")
        print("============")
        print("============")
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
            print("success send")
        except Exception as e:
            print(e)
    


    


@receiver(post_save, sender=m.RemedialMedicalHistory)
def historyPostSave(sender, instance, **kwargs):

    remedial_client_info = instance.remedial_client_info
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
                'client_id': remedial_client_info.client.id,
                'first_name':remedial_client_info.client.first_name,
                'last_name':remedial_client_info.client.last_name,
                'date_created': datetime.datetime.strftime(instance.date_created, "%d %b %Y %H:%M"),
                'receipt_image': instance.receipt_image.url if instance.receipt_image else ""
            }
            
        }
    )



# @receiver(post_save, sender=m.RemedialMedicalHistory)
# def historyPostSave(sender, instance, **kwargs):

#     remedial_client_info = instance.remedial_client_info

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'dashboard_consumer',
#         {
#             'type': 'send_data',
#             'action_type': 'add_remedial_client',
#             'payload':{
#                 'id': remedial_client_info.id,
#                 'first_name':remedial_client_info.client.first_name,
#                 'last_name':remedial_client_info.client.last_name,
#                 'health_insurance_number':str(remedial_client_info.health_insurance_number),
#                 'suffix': str(remedial_client_info.suffix)
#             }
            
#         }
#     )