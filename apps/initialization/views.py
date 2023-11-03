from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

from apps.authentication.models import (
    Student,
    Teacher,
    Parent,
    Group,
    Lesson,
    User
)
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    GroupSerializer,
    ParentSerializer,
    LessonSerializer,
    CustomAdminForDataItSelfSerializer,
    AsyncLessonSerializer
)

from apps.comment.models import StudentCommentFromTeacher, CommentReplyToTeacherFromParent
from apps.comment.serializers import StudentCommentFromTeacherSerializer, CommentReplyToTeacherFromParentSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from apps.permissions import permissions as custom_permissions

from .tasks import get_each_student_data

import datetime
import json
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    """
    Bu yerda barcha api endpointlarini ko'rish mumkin
    student --- studentlar ro'yxati
    teacher --- o'qituvchilar ro'yxati
    group --- guruhlar ro'yxati
    parent --- ota-onalar ro'yxati
    lesson --- darslar ro'yxati
    admin -- adminlar ro'yxati
    """
    return Response({
        'students': reverse('student-general', request=request, format=format),
        'teachers': reverse('teacher-general', request=request, format=format),
        'groups': reverse('group-general', request=request, format=format),
        'parents': reverse('parent-general', request=request, format=format),
        'admins': reverse('admin-general', request=request, format=format),
        'lessons': reverse('lesson-general', request=request, format=format),
    })


class CustomAdminDataAPIView(mixins.ListModelMixin,
                             generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CustomAdminForDataItSelfSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        return User.objects.filter(is_admin=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StudentGeneralViewForAdmins(mixins.ListModelMixin,
                                  generics.GenericAPIView):
    """
    Bu yerda studentlar ro'yxatini olish uchun view yaratiladi
    bu bilan birgalikda student profile ham ko'rinadi
    student profile --- bundan tashqari student profile update qilsa ham bo'ladi
    user --- Umumiy Userlarning malumotlari, bunga studenting shaxsiy malumotlarni kirmaydi
    parent -- Studentga biriktirilgan Ota Onaning umumiy maluotlari
    attendance -- studentning darga qatnashganligi yoki yo'qligi uchun (come=True -- kelgan, False kelmagan)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, *args, **kwargs):
        try:
            # logger.info("Working to get student data") log for data when production
            return self.list(request, *args, **kwargs)
        except Exception as e:
            logger.error("Student data is not found here. Detailed error message is: %s" % e)


class TeacherGeneralViewForAdmins(mixins.ListModelMixin,
                                  generics.GenericAPIView):
    """"
    Bu yerda o'qituvchilar ro'yxatini olish uchun view yaratiladi
    user -- Userning umumiy ma'lumotlar, bunga shaxsiy teacher malumotlarni kirmaydi
    teacher-profile -- teacherning profile qismi (avatar)
    lookup_field -- bittalik o'qituvchini olish uchun slug yani username orqali olinadi
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class StudentDetailApiView(mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    """
    Bittalik studentlik olish uchun endpoint
    slug -- har bir studenti uning slug orqali olinadi (slug bu username)
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'slug'

    permission_classes = (IsAuthenticated,)

    # @method_decorator(cache_page(60 * 60 * 2))
    # deploy qilgan paytda yoqib qo'yish kerak
    # agar cache bilan ishlash kerak bo'lganda
    def get(self, request, *args, **kwargs):
        # try:
        #     task_result = get_each_student_data.delay(kwargs["slug"])
        #     result = task_result.get()
        #     if result is None:
        #         return Response({"error": "Siz izlayotgan page topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        #     return Response(json.loads(result), status=status.HTTP_200_OK)
        # except Exception as x:
        #     return Response({"error": str(x)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return self.retrieve(request, *args, **kwargs)


class StudentProfileUpdateView(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               generics.GenericAPIView):
    """
    studenting profile qismini update qilish uchun
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        """
        Bu funksiya orqali faqat admin yoki studentlar o'zlarining profilizni o'zgartiradi
        savol --- student o'zini profili o'zgartira oladimi?, yoki faqat admin bunga ruxsatga egami?
        1. bu yerda student o'zini profili o'zgartira oladi
        2. 108 qatorni commentdan chiqarib qo'yilsa, va 100dan 106gacha comment qilinsa, faqat admin o'zgartira oladi
        """
        try:
            if self.request.user.is_student or self.request.user.is_admin:
                return self.retrieve(request, *args, **kwargs)
            else:
                raise NotFound(
                    detail="Siz izlayotgan page topilmadi", code=404)
        except ValueError as e:
            raise NotFound(detail="Siz izlayotgan page topilmadi", code=404)

        # return self.retrieve_by_slug(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DeleteStudentAPIView(mixins.DestroyModelMixin,
                           generics.GenericAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TeacherDetailApiView(mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    """
    har bir teacherning bittalik malumotlarini olish
    slug -- har bir teacher uning slug orqali olinadi (slug bu username)
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TeacherProfileUpdateView(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               generics.GenericAPIView):
    """
    bu yerda teacherning malumotlari olinadi
    slug -- bu teacherning username, Url endpointdan slug orqali olinadi
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'slug'
    """ shu yerda teacher profileni o'zi o'zgartira oladimi
     yoki faqat admin bunga ruxsatga egami
    shunga qarab permission yoziladi"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Bu funksiya orqali faqat admin yoki teacher o'zlarining profilizni o'zgartiradi
        1. bu yerda teacher o'zini profili o'zgartira oladi
        2. 108 qatorni commentdan chiqarib qo'yilsa, va 100dan 106gacha comment qilinsa, faqat admin o'zgartira oladi
        """
        try:
            if self.request.user.is_teacher or self.request.user.is_admin:
                return self.retrieve(request, *args, **kwargs)
            else:
                raise NotFound(
                    detail="Siz izlayotgan page topilmadi", code=404)
        except ValueError as e:
            raise NotFound(detail="Siz izlayotgan page topilmadi", code=404)

        # return self.retrieve_by_slug(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ParentGeneralViewForAdmins(mixins.ListModelMixin,
                                 generics.GenericAPIView):
    """
    bu yerda parenting malumotlarn olinadi
    """
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ParentDetailAPIView(mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GroupApiView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    """
    bu yerda dastur ichidagi barcha group malumotlari bor
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GroupApiDetailView(mixins.RetrieveModelMixin,
                         generics.GenericAPIView):
    """
    Bu yerda groupning bittalik malumotlarni olinadi
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'pk'
    """
    bu yerda barcha student, teacher, parentlar guruh malumotlarini olaadimi?
    bu yoki cheklangan holatda bo'ladimi
    hozirgi holatda barcha authenticatsiyadn o'tgan user ko'ra oladi
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GroupAPIUpdateView(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         generics.GenericAPIView):
    """
    Bu yerda groupning bittalik malumotlarni update qilish uchun view api
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'pk'

    permission_classes = (
        IsAuthenticated, custom_permissions.CurrentUserIsTeacher,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LessonApiView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    """Bu yerda ham barcha authentikatsiyadan o'tgan user lesson malumotlarni ko'ra oladi
    yoki teacher va studentga qarab permission yoziladi
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     """
    #     biz aslida alohida lesson yaratmaymiz, group yaratganda avtomatik ravishda lesson yaratiladi
    #     bu shunchaki test uchun yaratilgan
    #     """
    #     return self.create(request, *args, **kwargs)


class LessonApiDetailView(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'pk'
    """Bu yerda admin va teacher darslarni update, qila oladi"""
    permission_classes = (
        IsAuthenticated, custom_permissions.CurrentUserIsTeacher,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CreateLessonApiView(mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    """Bu yerda admin va teacher darslarni create, qila oladi. va yana qanday holatlarda permission yoki throttle yoziladi (throttle bu requestlarni cheklash uchun)"""
    permission_classes = (
        IsAuthenticated, custom_permissions.CurrentUserIsTeacher,)

    def perform_create(self, serializer):
        group_id = self.kwargs['pk']
        group = Group.objects.get(id=group_id)
        serializer.save(group=group)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DeleteLessonAPIView(mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'pk'
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentCommentFromTeacherApiView(mixins.ListModelMixin,
                                       mixins.CreateModelMixin,
                                       generics.GenericAPIView):
    queryset = StudentCommentFromTeacher.objects.all()
    serializer_class = StudentCommentFromTeacherSerializer
    """Bu Viewsda faqat teacher uchun studentga comment yozish qismi qilingan. Parent, Admin lar uchun alohida comment yozish qismi qilinadi"""
    permission_classes = (
        IsAuthenticated, custom_permissions.CurrentUserIsTeacher, )

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        lesson_id = self.kwargs["lesson_id"]
        try:
            if self.request.user.is_teacher:
                teacher = Teacher.objects.get(user=self.request.user)
                student = Student.objects.get(id=student_id)
                lesson = Lesson.objects.get(id=lesson_id)
                serializer.save(student=student,
                                lesson=lesson, teacher=teacher)
            else:
                raise NotFound(
                    detail="Siz izlayotgan page topilmadi", code=404)
        except ValueError as e:
            raise NotFound(detail="Siz izlayotgan page topilmadi", code=404)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


'''
class CommentReplyToTeaacherAPIView(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    generics.GenericAPIView):
    
    queryset = CommentReplyToTeacher.objects.all()
    serializer_class = CommentReplyToTeacherSerializer
    """Har bitta student o'ziga teacher orqali yo'zilgan commentga javob qaytara olishi 
    uchun yozilga views. Authentikatasiyadan o'tgan user student bo'lishi shart"""
    permission_classes = (IsAuthenticated, custom_permissions.CurrentUserIsStudent,)

    def perform_create(self, serializer):
        comment_id = self.kwargs["comment_id"]
        try:
            if self.request.user.is_student:
                student = Student.objects.get(user=self.request.user)
                comment = StudentCommentFromTeacher.objects.get(id=comment_id)
                serializer.save(comment=comment, student=student)
            else:
                raise NotFound(detail="Siz izlayotgan page topilmadi", code=404)
        except ValueError as e:
            raise NotFound(detail="Sizda qandaydur muammo bor %s" % e)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''


class CommentReplyToTeacherFromParentView(mixins.ListModelMixin,
                                          mixins.CreateModelMixin,
                                          generics.GenericAPIView):
    queryset = CommentReplyToTeacherFromParent.objects.all()
    serializer_class = CommentReplyToTeacherFromParentSerializer
    """Har bitta parent o'zining o'gliga teacher orqali yo'zilgan commentga javob qaytara olishi 
    uchun yozilga views. Authentikatasiyadan o'tgan user parent bo'lishi shart"""
    permission_classes = (
        IsAuthenticated, custom_permissions.CurrentUserIsParent,)

    def perform_create(self, serializer):
        comment_id = self.kwargs["comment_id"]
        try:
            if self.request.user.is_parent:
                parent = Parent.objects.get(user=self.request.user)
                comment = StudentCommentFromTeacher.objects.get(id=comment_id)
                serializer.save(comment=comment, parent=parent)
            else:
                raise NotFound(
                    detail="Siz izlayotgan page topilmadi", code=404)
        except ValueError as e:
            raise NotFound(detail="Sizda qandaydur muammo bor %s" % e)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentDeleteAPIView(mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = StudentCommentFromTeacher.objects.all()
    serializer_class = StudentCommentFromTeacherSerializer
    permission_classes = (permissions.AllowAny,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, APIException):
            problem = {
                "title": exc.get_full_details(),
                "status": exc.status_code,
                "detail": str(exc),
            }
            return Response(data=problem, status=exc.status_code)
        else:
            problem = {
                "title": "Ichki hato yuz berdi",
                "status": 500,
                "detail": "Backend tizimdan muammo chiqdi",
            }
            return Response(data=problem, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


@requires_csrf_token
def not_found(request, exception):
    return JsonResponse(
        {"hato": "Siz izlayotgan sahifa topilmadi. Iltimos to'gri manzil kiriting"},
        status=404
    )


# this is for async and real time websocket
@api_view(['GET'])
def get_lesson_data(request):
    """
    Bu yerda darslar malumotlari olinadi
    """
    if request.method == "GET":
        lessons = Lesson.objects.all()
        serializer = AsyncLessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Bu endpoint faqat GET methodi bilan ishlaydi"}, status=status.HTTP_400_BAD_REQUEST)
