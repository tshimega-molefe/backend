from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from emergency.decorators import role_required
from emergency.models import Emergency
from emergency.serializers import EmergencySerializer

class EmergencyConsumer(AsyncJsonWebsocketConsumer):
 
    @database_sync_to_async
    def db_create_emergency(self, data):
        serializer = EmergencySerializer(data=data, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        
        return serializer.create(serializer.validated_data)
    
    @database_sync_to_async
    def db_update_emergency(self, data):
        instance = Emergency.objects.get(id=data.get('id'))
        serializer = EmergencySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.update(instance, serializer.validated_data)

    @database_sync_to_async
    def db_get_user_emergencys(self): 
        user_role = self.user.get_role_display()
        excluded_statuses = [Emergency.Status.COMPLETED, Emergency.Status.CANCELLED]

        if user_role == 'SECURITY':
            emergency_ids = self.user.security.emergencys_as_security.exclude(status__in = excluded_statuses)
        else: 
            emergency_ids = self.user.citizen.emergencys_as_citizen.exclude(status__in = excluded_statuses)
        
        serializer = EmergencySerializer(emergency_ids, many=True)

        return serializer.data

    @database_sync_to_async
    def db_accept_emergency(self, data):
        instance = Emergency.objects.get(id=data['id'])
        instance.status = Emergency.Status.ACCEPTED
        instance.security = self.user.security
        
        serializer = EmergencySerializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
                
        return serializer.save()

    @database_sync_to_async
    def db_complete_emergency(self, data):
        instance = Emergency.objects.get(id=data['id'])
        instance.status = Emergency.Status.COMPLETED
        
        serializer = EmergencySerializer(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        
        return serializer.save()

    async def create_emergency(self, message):        
        emergency = await self.db_create_emergency(message)

        await self.channel_layer.group_send('SECURITY',  
                {
                    'type': 'echo.message',
                    'id': f'{emergency.id}',
                    'username': self.user.username,
                }
        )

        await self.channel_layer.group_add(f'{emergency.id}', self.channel_name)

    async def accept_emergency(self, message):        
        emergency = await self.db_accept_emergency(message)

        await self.channel_layer.group_add(f'{emergency["id"]}', self.channel_name)
        await self.channel_layer.group_send(f'{emergency["id"]}',
            {
                'type': 'echo.message',
                'data': f'{emergency}'
            }
        )

    async def complete_emergency(self, message):        
        emergency = await self.db_complete_emergency(message)

        await self.channel_layer.group_send(f'{emergency["id"]}',
            {
                'type': 'echo.message',
                'data': f'{emergency}'
            }
        )

    async def echo_message(self, data):
        return await self.send_json(data)

    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.accept()

            if self.user.get_role_display() == "SECURITY":
                await self.channel_layer.group_add(f'{self.user.get_role_display()}', self.channel_name)
                
            elif self.user.get_role_display() == "CITIZEN":
                for trip in await self.db_get_user_emergencys():
                    await self.channel_layer.group_add(trip["id"], self.channel_name)
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
        elif message_type == 'accept.emergency':
            await self.accept_emergency(content)
        elif message_type == 'complete.emergency':
            await self.complete_emergency(content)

        return await super().receive_json(content, **kwargs)