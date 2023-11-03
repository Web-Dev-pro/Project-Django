from celery import shared_task
from apps.authentication.models import (
    Student,
    User
)
from .serializers import (
    LessonSerializer,
    StudentSerializer,
)
import json
from datetime import date, time, datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, time)):
            return obj.isoformat()  # Convert date to ISO format
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return super().default(obj)

@shared_task
def get_student_data():
    try:
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        json_data = json.dumps(serializer.data, cls=CustomJSONEncoder)
        return json_data
    except Student.DoesNotExist:
        return None

@shared_task
def get_each_student_data(slug):
    try:
        student = Student.objects.get(slug=slug)
        serializer = StudentSerializer(student, many=False)
        json_data = json.dumps(serializer.data, cls=CustomJSONEncoder)
        return json_data
    except Student.DoesNotExist:
        return None