# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("admin_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def new_request(self, event):
        message = json.loads(event["message"])
        await self.send(text_data=json.dumps({"type": "new_request", "data": message}))
