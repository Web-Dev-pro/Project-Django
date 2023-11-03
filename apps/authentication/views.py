from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.db import IntegrityError, transaction
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.initialization.serializers import AdminSerializer
from .models import User
from .serializers import (
    CustomParentRegistrationSerializer,
    CustomStudentRegistrationSerializer,
    CustomTeacherRegistrationSerializer,
    CustomLoginSerializer,
)


class CustomTokenPairSerializer(TokenObtainPairSerializer):
    """
    Bu yerda tokenlarni olish uchun serializer yaratiladi
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token["phone_number"] = str(user.phone_number)
        token["is_admin"] = user.is_admin
        token['is_student'] = user.is_student
        token['is_teacher'] = user.is_teacher
        token['is_parent'] = user.is_parent
        return token


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer


@api_view(["GET"])
def api_root(request, format=None):
    """
    Bu yerda barcha STUDENT, PARENT VA TEACHER UCHUN API ENDPOINTLARINI KO'RISH UCHUN VIEW YARATILDI
    students --- STUDENT uchun API register qilish uchun endpoint
    teachers --- TEACHER uchun API register qilish uchun endpoint
    groups --- GROUP uchun API register qilish uchun endpoint
    parents --- PARENT uchun API register qilish uchun endpoint
    token obtain --- login qilish uchun endpoint
    token refresh --- tokenni yangilash uchun endpoint
    """
    return Response({
        "Teacher Register": reverse("teacher_register", request=request, format=format),
        "Parent Register": reverse("parent_register", request=request, format=format),
        "Student Register": reverse("student_register", request=request, format=format),
        "Admin Register": reverse("admin_register", request=request, format=format),
        "token obtain login": reverse("token_obtain_pair", request=request, format=format),
        "token refresh": reverse("token_refresh", request=request, format=format),
    })


class CustomAdminRegistrationView(generics.CreateAPIView):
    serializer_class = AdminSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        admin = serializer.save()
        admin.is_admin = True
        admin.save()
        return admin


class CustomTeacherRegistrationView(RegisterView):
    """
    Bu yerda Teacher uchun registration view yaratiladi
    """
    serializer_class = CustomTeacherRegistrationSerializer

    def get_queryset(self):
        """
        Bu yerda default queryset yo'qligi uchun menga assertion error chiqib qoldi
        shun uchun bu methodni override qilishim kerak bo'ldi va hech qanday qiymat qaytarishim kerak bo'lmadi
        lekin muammoni hal qiladi
        AssertionError: 'CustomTeacherRegistrationView' should either include a `queryset` attribute, or override the `get_queryset()` method.
        """
        return None

    def create(self, request, *args, **kwargs):
        """
        Bu yerda user uchun registration view yaratiladi
        key --- bu yani har bir user uchun unique bo'lgan kalit, va bu kalitni auto create qilmadim
        login --- yani auto login bo'lib ketishini oldini olish uchun
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = serializer.save(self.request)
            return Response({"malumot": "Teacher Muvaffaqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
        except IntegrityError as i:
            if "UNIQUE constraint" in str(i) and "phone_number" in str(i):
                return Response({"error": "Bu raqamdagi foydalanuvchi allaqchon bor"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({f"malumot": "Ichki hato. Integrity errorni boshqa ko'rinishi bor. {i}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as i:
            return Response({f"malumot": "Ichki hato. {i}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomParentRegistrationView(RegisterView):
    serializer_class = CustomParentRegistrationSerializer

    def get_queryset(self):
        """
        Bu yerda default queryset yo'qligi uchun menga assertion error chiqib qoldi
        shun uchun bu methodni override qilishim kerak bo'ldi va hech qanday qiymat qaytarishim kerak bo'lmadi
        lekin muammoni hal qiladi
        AssertionError: 'CustomTeacherRegistrationView' should either include a `queryset` attribute, or override the `get_queryset()` method.
        """
        return None

    def create(self, request, *args, **kwargs):
        """
        Bu yerda Userlar uchun registration view yaratiladi
        key --- bu yani har bir user uchun unique bo'lgan kalit, va bu kalitni auto create qilmadim
        login --- yani auto login bo'lib ketishini oldini olish uchun
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                parent = serializer.save(self.request)
            return Response({"detail": "Parent muvaffaqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
        except IntegrityError as i:
            if "UNIQUE constraint" in str(i) and "phone_number" in str(i):
                return Response({"error": "Bu raqamdagi user allaqchon bor"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": f"Ichki hato. Integrity errorni boshqa ko'rinishi bor. {i}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Ichki hato. {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomStudentRegistrationView(RegisterView):
    serializer_class = CustomStudentRegistrationSerializer

    def get_queryset(self):
        """
        Bu yerda default queryset yo'qligi uchun menga assertion error chiqib qoldi
        shun uchun bu methodni override qilishim kerak bo'ldi va hech qanday qiymat qaytarishim kerak bo'lmadi
        lekin muammoni hal qiladi
        AssertionError: 'CustomTeacherRegistrationView' should either include a `queryset` attribute, or override the `get_queryset()` method.
        """
        return None

    def create(self, request, *args, **kwargs):
        """
        Bu yerda Student uchun registration view yaratiladi
        key --- bu yani har bir student uchun unique bo'lgan kalit, va bu kalitni auto create qilmadim
        login --- yani auto login bo'lib ketishini oldini olish uchun
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                student = serializer.save(self.request)
            return Response({"detail": "Student muvaffaqiyatli yaratildi"}, status=status.HTTP_201_CREATED)
        except IntegrityError as i:
            if "UNIQUE constraint" in str(i) and "phone_number" in str(i):
                return Response({"error": "Bu raqamdagi student allaqchon bor"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": f"Ichki hato. Integrity errorni boshqa ko'rinishi bor. {i}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as i:
            return Response({"error": f"Ichki hato. {i}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
