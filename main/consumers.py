import json
import datetime

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import main.models as m

class DashboardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)('dashboard_consumer', self.channel_name)
        
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())

        # recently added remedial client  
        recently_added_client = m.RemedialClientInfo.objects\
            .select_related("client")\
            .filter(date_created__gte=today)\
            .order_by("date_created")\
            .values("id", "client__id", "client__first_name", "client__last_name", "health_insurance_number", "suffix", "date_created")

        recently_added_client_container = []
        
        for client in recently_added_client:
            recently_added_client_container.append({
                "id": client["id"],
                "client_id": client["client__id"],
                "first_name": client["client__first_name"],
                "last_name": client["client__last_name"],
                "health_insurance_number": str(client["health_insurance_number"]),
                "suffix": str(client["suffix"]),
                "date_created": datetime.datetime.strftime(client["date_created"], "%d %b %Y %H:%M")
            })

        self.send(text_data=json.dumps({
            "action_type": "init_remedial_client",
            "payload": recently_added_client_container
        }))


        # require receipt 
        require_receipts = m.RemedialMedicalHistory.objects\
            .select_related("remedial_client_info","remedial_client_info__client")\
            .filter(date_created__gte=today)\
            .values(
                "id",
                "remedial_client_info__client__id",
                "remedial_client_info__client__first_name",
                "remedial_client_info__client__last_name",
                "date_created",
                "receipt_image"
            )
        
        require_receipt_container = []

        for require_receipt in require_receipts:
            require_receipt_container.append({
                "id":require_receipt["id"],
                "client_id": require_receipt["remedial_client_info__client__id"],
                "first_name":require_receipt["remedial_client_info__client__first_name"],
                "last_name":require_receipt["remedial_client_info__client__last_name"],
                "date_created":datetime.datetime.strftime(require_receipt["date_created"], "%d %b %Y %H:%M"),
                "receipt_image": require_receipt["receipt_image"]
            })
        
        self.send(text_data=json.dumps({
            "action_type": "init_remedial_history",
            "payload": require_receipt_container
        }))

        # missing receipt 
        missing_receipts = m.RemedialMedicalHistory.objects\
            .select_related("remedial_client_info","remedial_client_info__client")\
            .filter(receipt_image="",date_created__lte=today)\
            .values(
                "id",
                "remedial_client_info__client__id",
                "remedial_client_info__client__first_name",
                "remedial_client_info__client__last_name",
                "date_created",
                "receipt_image"
            )
        
        missing_receipt_container = []

        for missing_receipt in missing_receipts:
            missing_receipt_container.append({
                "id":missing_receipt["id"],
                "client_id": missing_receipt["remedial_client_info__client__id"],
                "first_name":missing_receipt["remedial_client_info__client__first_name"],
                "last_name":missing_receipt["remedial_client_info__client__last_name"],
                "date_created":datetime.datetime.strftime(missing_receipt["date_created"], "%d %b %Y %H:%M"),
                "receipt_image": missing_receipt["receipt_image"]
            })
        
        self.send(text_data=json.dumps({
            "action_type": "init_missing_receipt",
            "payload": missing_receipt_container
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('dashboard_consumer', self.channel_name) 
        pass

    def receive(self, text_data):

        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
    def send_data(self, data, type="send_data"):
        
        print("===================1231231@")
        print(data)
        self.send(text_data=json.dumps(data))
    # def send(self, data):
    #     self.send(text_date=json.dumps(data))