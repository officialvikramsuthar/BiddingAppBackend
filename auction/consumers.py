# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Item
from .serializers import ItemSerializer
from asgiref.sync import sync_to_async


class ItemConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("items", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("items", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        item_id = data['item_id']
        bid = data['bid']

        item = await sync_to_async(Item.objects.get)(id=item_id)
        item.current_bid = bid
        await sync_to_async(item.save)()

        item_data = ItemSerializer(item).data
        await self.channel_layer.group_send(
            "items",
            {
                "type": "item.update",
                "item": item_data
            }
        )

    async def item_update(self, event):
        item = event["item"]
        await self.send(text_data=json.dumps(item))
