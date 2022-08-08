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
                    
        recently_added_client = m.RemedialClientInfo.objects\
            .select_related("client")\
            .filter(date_created__gte=today)\
            .order_by("date_created")\
            .values("client__first_name", "client__last_name", "health_insurance_number", "suffix", "date_created")

        recently_added_client_container = []
        for client in recently_added_client:
            recently_added_client_container.append({
                "first_name": client["client__first_name"],
                "last_name": client["client__last_name"],
                "health_insurance_number": str(client["health_insurance_number"]),
                "suffix": str(client["suffix"]),
                "date_created": datetime.datetime.strftime(client["date_created"], "%d %b %Y %H:%M:%S")
            })
            
        self.send(text_data=json.dumps({
            "action_type": "init_remedial_client",
            "payload": recently_added_client_container
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
        self.send(text_data=json.dumps(data))
    # def send(self, data):
    #     self.send(text_date=json.dumps(data))