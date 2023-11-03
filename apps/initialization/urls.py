from django.urls import path, include
from . import views, attendance, mark

urlpatterns = [
    path('', views.api_root, name='api-root'),
    # students
    path('students/', views.StudentGeneralViewForAdmins.as_view(), name='student-general'),
    path('student/<slug:slug>/', views.StudentDetailApiView.as_view(), name='student-detail'),
    path('student/<slug:slug>/update/', views.StudentProfileUpdateView.as_view(), name='student-update'),
    path('student/<slug:slug>/delete/', views.DeleteStudentAPIView.as_view(), name='student-delete'),
    # teachers
    path('teachers/', views.TeacherGeneralViewForAdmins.as_view(), name='teacher-general'),
    path('teacher/<slug:slug>/', views.TeacherDetailApiView.as_view(), name='teacher-detail'),
    path('teacher/<slug:slug>/update/', views.TeacherProfileUpdateView.as_view(), name='teacher-update'),
    # parent
    path('parents/', views.ParentGeneralViewForAdmins.as_view(), name='parent-general'),
    path("parent/<slug:slug>/", views.ParentDetailAPIView.as_view(), name="parent-detail"),
    #admins
    path('admins/', views.CustomAdminDataAPIView.as_view(), name='admin-general'),
    # lesson
    path('lessons/', views.LessonApiView.as_view(), name="lesson-general"),
    path('lesson/<int:pk>/', views.LessonApiDetailView.as_view(), name="lesson-detail"),
    path("lesson/<int:pk>/delete/", views.DeleteLessonAPIView.as_view(), name="lesson-delete"),
    # Group
    path('groups/', views.GroupApiView.as_view(), name="group-general"),
    path('group/<int:pk>/', views.GroupApiDetailView.as_view(), name="group-detail"),
    path('group/<int:pk>/lesson-create/', views.CreateLessonApiView.as_view(), name="lesson-create"),
    path('group/<int:pk>/update/', views.GroupAPIUpdateView.as_view(), name="group-update"),
    # attendance
    path('group/<int:group_id>/student/<int:student_id>/lesson/<int:lesson_id>/attendance/<int:attendance_id>/', attendance.UpdateGroupAttendanceView.as_view(), name='group-attendance-update'),
    # mark
    path("group/<int:group_id>/student/<int:student_id>/lesson/<int:lesson_id>/mark/<int:mark_id>/", mark.MarkUpdateAPIView.as_view(), name="group-mark-update"),
    # comment
    path('comment/student/<int:student_id>/lesson/<int:lesson_id>/', views.StudentCommentFromTeacherApiView.as_view(), name='student-comment'),
    # path("comment/reply/<int:comment_id>/", views.CommentReplyToTeaacherAPIView.as_view(), name="reply_to_teacher"),
    path("comment/reply/parent/<int:comment_id>/", views.CommentReplyToTeacherFromParentView.as_view(), name="reply_to_teacher_from_parent"),
    # delete comment
    path("comment/<int:pk>/delete/", views.CommentDeleteAPIView.as_view(), name="comment-delete"),
    # confgure routing for consumers
]
