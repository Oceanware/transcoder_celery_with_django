from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User


class VideoConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['url_route']['kwargs']
        user = await sync_to_async(User.objects.get, thread_sensitive=True)(id=user['id'])
        await self.accept()
        await self.channel_layer.group_add(str(user.id), self.channel_name)

        print(user.id)
        if user.is_staff:
            print('admin_notifications 1')
            await self.channel_layer.group_add("admin_notifications", self.channel_name)

    async def disconnect(self, code):
        user = self.scope['url_route']['kwargs']
        user = await sync_to_async(User.objects.get, thread_sensitive=True)(id=user['id'])
        if user.is_staff:
            await self.channel_layer.group_discard("admin_notifications", self.channel_name)

    async def admin_pusher(self, event):
        await self.send_json(event)
