from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, generics

from apps.authentication.models import Attendance
from apps.initialization.serializers import AttendanceSerializer


class UpdateGroupAttendanceView(mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                generics.GenericAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student__id=student_id, student__group_id=group_id)

    def get_object(self):
        queryset = self.get_queryset()
        lesson_id = self.kwargs['lesson_id']
        attendance_id = self.kwargs['attendance_id']
        obj = get_object_or_404(queryset, lesson__id=lesson_id, id=attendance_id)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
