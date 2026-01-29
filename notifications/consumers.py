# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         user = self.scope["user"]

#         if user.is_anonymous:
#             await self.close()
#             print("Anonymous user tried to connect, connection closed.")
#         else:
#             # Each user has a personal group
#             self.group_name = f"user_{user.id}"

#             # Add this connection to the user's group
#             await self.channel_layer.group_add(
#                 self.group_name,
#                 self.channel_name
#             )

#             await self.accept()
#             print(f"WebSocket CONNECTED user_{user.id}")

#     async def disconnect(self, close_code):
#         # Remove from group on disconnect
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#         print(f"WebSocket CLOSED user_{self.scope['user'].id}, code: {close_code}")

#     async def receive(self, text_data):
#         """
#         Optional: handle messages sent from the client to the server.
#         Right now we don't need it, but it's here for future use.
#         """
#         data = json.loads(text_data)
#         message = data.get("message", "")
#         print(f"Received message from client: {message}")

#     async def send_notification(self, event):
#         """
#         Server sends notifications to this consumer.
#         Event must have a 'message' key.
#         """
#         await self.send(text_data=json.dumps({
#             "message": event["message"]
#         }))
#         print(f"Notification sent to user_{self.scope['user'].id}: {event['message']}")