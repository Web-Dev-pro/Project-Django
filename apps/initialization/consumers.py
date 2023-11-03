from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time
from . import tasks
from core import celery

class StudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'students'  # Group name for all student updates
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_student(self, event):
        text_message = event["text"]

        if isinstance(text_message, dict):
            text_message = json.dumps(text_message)

        await self.send(text_message)

    
class EachStudentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        get student id from url is given to routing.py file using self.scope
        """
        self.student_username = self.scope["url_route"]["kwargs"]["student_username"]
        self.group_name = "student_each_data"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_each_student_data(self, event):
        text_message = event["text"]
        

        if isinstance(text_message, dict):
            text_message = json.dumps(text_message)

        await self.send(text_message)
        celery.process_each_student_data.delay(self.student_username)