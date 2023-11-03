from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.api_root),
    path('register/teacher/', views.CustomTeacherRegistrationView.as_view(), name='teacher_register'),
    path('register/continue-student/parent/', views.CustomParentRegistrationView.as_view(), name='parent_register'),
    path('register/student/', views.CustomStudentRegistrationView.as_view(), name='student_register'),
    path('register/admin/', views.CustomAdminRegistrationView.as_view(), name='admin_register'),
    # for login
    path('login/', views.CustomLoginView.as_view(), name='login'),
    # for jwt
    path('token/login/', views.CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]