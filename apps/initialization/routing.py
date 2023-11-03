from django.urls import re_path
from . import consumers
"""
I may use it later on depends on situations. Like real time notifications or chats to be considered
"""
# websocket_urlpatterns = [  
#     re_path(r"ws/students/$", consumers.StudentConsumer.as_asgi()),
#     re_path(r"ws/student/(?P<student_username>\w+)/$", consumers.EachStudentConsumer.as_asgi()),
# ]