from urllib import request
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from emergency.decorators import role_required
from emergency.serializers import EmergencySerializer
from user.models import User
class EmergencyConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def db_create_emergency(self, request, **kwargs):
        serializer = EmergencySerializer(data=request, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)

    async def create_emergency_echo(self, data):
        return await self.send_json(data)

    async def create_emergency(self, message):        
        emergency = await self.db_create_emergency(message, user=self.user)

        await self.channel_layer.group_send('SECURITY',  
                {
                    'id': f'{emergency.id}',
                    'type': 'create.emergency.echo',
                    'username': self.user.username,
                }
        )

    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.accept()

            if self.user.get_role_display() == "SECURITY":
                await self.channel_layer.group_add(f'{self.user.get_role_display()}', self.channel_name)
            elif self.user.get_role_display() == "CITIZEN":
                await self.channel_layer.group_add(f'{self.user.get_role_display()}', self.channel_name)
        else: 
            await self.close(code=401)

    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                f'{self.user.id}',
                self.channel_name
            )
        
        await super().disconnect(code=code)

    async def receive_json(self, content, **kwargs):
        message_type = content['type']
        if message_type == 'create.emergency':
            await self.create_emergency(content)
            

        return await super().receive_json(content, **kwargs)
