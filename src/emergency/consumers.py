from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from emergency.decorators import role_required
from emergency.models import Emergency
from emergency.serializers import EmergencySerializer
from user.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class EmergencyConsumer(AsyncJsonWebsocketConsumer):
 
    @database_sync_to_async
    def get_user(self, validated_token):
        try:
            user = get_user_model().objects.get(id=validated_token['user_id'])
            return user

        except User.DoesNotExist:
            return AnonymousUser()

    @database_sync_to_async
    def db_get_user_emergencys(self): 
        user_role = self.scope['user'].get_role_display()
        included_statuses = [Emergency.Status.REQUESTED, Emergency.Status.ACCEPTED, Emergency.Status.IN_PROGRESS]
        
        if user_role == 'SECURITY':
            emergencies_matched = Emergency.objects.filter(status__in=included_statuses, security=self.scope['user'].security)
        else: 
            emergencies_matched = Emergency.objects.filter(status__in=included_statuses, citizen=self.scope['user'].citizen)

        emergencies = []
        for emergency in emergencies_matched:
            emergencies.append(emergency)

        return emergencies

    @database_sync_to_async
    def db_get_emergency(self, id):
        emergency = Emergency.objects.get(id=id)

        return emergency

    @database_sync_to_async
    def db_create_emergency(self, user):
        emergency = Emergency.objects.create(citizen=user.citizen)
        return emergency
        

    @database_sync_to_async
    def db_cancel_emergency(self, id):
        emergency = Emergency.objects.get(id=id)
        emergency.status = Emergency.Status.CANCELLED
        emergency.save()

        return emergency
    
    @database_sync_to_async
    def db_accept_emergency(self, id, user):
        emergency = Emergency.objects.get(id=id)
        emergency.status = Emergency.Status.ACCEPTED
        emergency.security = user.security
        emergency.save()

        return emergency

    @database_sync_to_async
    def db_start_emergency(self, id):
        emergency = Emergency.objects.get(id=id)
        emergency.status = Emergency.Status.IN_PROGRESS
        emergency.save()

        return emergency


    @database_sync_to_async
    def db_complete_emergency(self, id):
        emergency = Emergency.objects.get(id=id)
        emergency.status = Emergency.Status.COMPLETED
        emergency.save()

        return emergency



    # * 





    # TODO: Change username -> citizen
    async def create_emergency(self, message):   
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id'],
                'username': message['username']
            }
        )

    async def cancel_emergency(self, message):        
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id']
            }
        )


    async def accept_emergency(self, message):
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id'],
                # 'security': message['security']
            }
        )

    async def update_emergency(self, message):   
        await self.send_json(message)
        


    async def start_emergency(self, message):        
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id']
            }
        )


    async def complete_emergency(self, message):        
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id']
            }
        )

    async def renew_emergency(self, message):
        await self.send_json(
            {
                'type': message['type'],
                'id': message['id'],
                'status': message['status']
            }
        )

    async def connect(self):
        await self.accept()
           
    async def disconnect(self, code):
        await super().disconnect(code=code)

    async def receive_json(self, content, **kwargs):
        
        #Make sure user is authorised to access websocket
        if self.scope['user'].id:
            message_type = content['type']

            #Emergency Creation
            if message_type == 'create.emergency':
                emergency = await self.db_create_emergency(user=self.scope['user'])
                
                await self.channel_layer.group_send(f"SECURITY",  
                    {
                        'type': 'create.emergency',
                        'id': f"{emergency}",
                        'username': f"{self.scope['user']}"
                    }
                )

                await self.channel_layer.group_send(f"{self.scope['user'].id}", 
                    {
                        'type': 'create.emergency',
                        'id': f"{emergency}",
                        'username': f"{self.scope['user']}",
                    }
                )
                
                await self.channel_layer.group_add(f"{emergency.id}", self.channel_name)

            #Emergency Cancellation
            elif message_type == 'cancel.emergency':
                
                emergency = await self.db_cancel_emergency(id=content['id'])

                await self.channel_layer.group_send(f"SECURITY",  
                    {
                        'type': 'cancel.emergency',
                        'id': f"{emergency.id}"
                    }
                )

                await self.channel_layer.group_send(f"{emergency.id}",  
                    {
                        'type': 'cancel.emergency',
                        'id': f"{emergency.id}"
                    }
                )

                await self.channel_layer.group_discard(f"{emergency.id}", self.channel_name)

            #Emergency Accepting
            elif message_type == 'accept.emergency':

                emergency = await self.db_accept_emergency(id=content['id'], user=self.scope['user'])
                
                await self.channel_layer.group_add(f'{emergency.id}', self.channel_name)
                await self.channel_layer.group_send(f"{emergency.id}",
                    {
                        'type': 'accept.emergency',
                        'id': f"{content['id']}",
                        # 'security': f"{self.scope['user']}"
                    }
                )

            #Emergency Start
            elif message_type == 'start.emergency':
                emergency = await self.db_start_emergency(id=content['id'])
                await self.channel_layer.group_send(f'{emergency.id}',
                {
                    'type': 'start.emergency',
                    'id': f'{emergency.id}'   
                })

            #Emergency Completion
            elif message_type == 'complete.emergency':
                emergency = await self.db_complete_emergency(id=content['id'])
                await self.channel_layer.group_send(f'{emergency.id}',
                    {
                        'type': 'complete.emergency',
                        'id': f'{emergency.id}'
                    }
                )

            elif message_type == 'update.location':

                # data = {
                #     'type': 'update.location',
                #     'id': f"{self.scope['user']}"
                # }
   
                # await self.channel_layer.group_send(f"{self.scope['user'].id}", data)
                
                for emergency in await self.db_get_user_emergencys():
                    data = {
                        'type': 'update.emergency',
                        'id': f'{emergency.id}',
                    }

                    if 'citizen' in content:
                        data['citizen'] = content['citizen']
                    
                    if 'security' in content: 
                        data['security'] = content['security']

                    await self.channel_layer.group_send(f'{emergency.id}', data) 

        #If user isnt authorised make the user send authorisation details or disconnect the user
        else: 
            try: 
                token = content['token']

                try:
                    # UntypedToken(token)                    
                    decoded_data = TokenBackend(algorithm="HS256").decode(token, verify=False)
                    self.scope['user'] = await self.get_user(validated_token=decoded_data)

                    await self.channel_layer.group_add(f"{self.scope['user'].id}", self.channel_name)
                    await self.channel_layer.group_add(f"{self.scope['user'].get_role_display()}", self.channel_name)

                    for emergency in await self.db_get_user_emergencys():
                        await self.channel_layer.group_add(f'{emergency.id}', self.channel_name) 

                        await self.channel_layer.group_send(f'{emergency.id}', 
                        {
                            'type': 'renew.emergency',
                            'id': f'{emergency.id}',
                            'status': f'{emergency.get_status()}'
                        })

                except (InvalidToken, TokenError) as e:
                    # Token is invalid
                    print(e)
                    await self.close(code=4001)

            except Exception as e:
                
                # Data is not valid, so close the connection.
                print(e)
                await self.close(code=4001)

        return await super().receive_json(content, **kwargs)