from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics

from apps.authentication.models import Mark
from .serializers import MarkSerializer


class MarkUpdateAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    serializer_class = MarkSerializer

    def get_queryset(self):
        """
        bu yerda urls orqali kelayotgan idlarni olib ularni serializer va model orqali olib chiqib
        deserializer qilish
        group_id -- bu group idsi yani url orqali keladi
        student_id -- bu student idsi yani url orqali keladi
        """
        group_id = self.kwargs["group_id"]
        student_id = self.kwargs["student_id"]
        return Mark.objects.filter(student__id=student_id, student__group_id=group_id)

    def get_object(self):
        queryset = self.get_queryset()
        lesson_id = self.kwargs["lesson_id"]
        mark_id = self.kwargs["mark_id"]
        obj = get_object_or_404(queryset, lesson__id=lesson_id, id=mark_id)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
