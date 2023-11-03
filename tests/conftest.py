import pytest
from mixer.backend.django import mixer
from apps.authentication.models import (
    Student,
    StudentProfile,
    Teacher,
    TeacherProfile,
    User,
    Mark,
    Lesson,
    Group,
    Parent
)
from django.test import RequestFactory
from rest_framework.test import APIClient

from apps.comment.models import StudentCommentFromTeacher
import itertools

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def created_group(teacher_factory):
    group = Group.objects.create(name="A2", teacher=teacher_factory())
    yield group

    group.delete()

@pytest.fixture
def student_factory(db, created_group):
    counter = itertools.count(start=1)
    def create_student():
        username = f"students{next(counter)}"
        phone_number = f"9989123465{next(counter):03d}"
        user = User.objects.create(username=username, phone_number=phone_number, password="qwerty1234", is_student=True)
        student = Student.objects.create(user=user, full_name="Second Omonov", age=24, group=created_group)
        return student

    return create_student

@pytest.fixture
def parent_factory(db, student_factory):
    def create_parent():
        user = User.objects.create(username="parent", phone_number="+998901112233", password="qwerty1234", is_parent=True)
        student = student_factory()
        parent = Parent.objects.create(user=user, student=student, full_name="Parent Olimov")
        return parent
    
    return create_parent

@pytest.fixture
def teacher_factory(db):
    counter = itertools.count(start=1)
    def create_teacher():
        username = f"teacher{next(counter)}"
        phone_number = f"+9989657898{next(counter):03d}"
        user = User.objects.create(username=username, phone_number=phone_number, password="qwerty1234", is_teacher=True)
        return Teacher.objects.create(user=user, full_name="Teacher Janobi")

    return create_teacher

@pytest.fixture
def group_factory(db):
    def create_group():
        return mixer.blend(Group)

    return create_group

@pytest.fixture
def mark_factory(db):
    def create_mark(student=None, lesson=None, mark=0):
        return mixer.blend(Mark, student=student, lesson=lesson, mark=mark)

    return create_mark

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def lesson_factory(db, created_group):
    def create_lesson():
        return mixer.blend(Lesson, group=created_group)

    return create_lesson

@pytest.fixture
def admin_factory(db):
    counter = itertools.count(start=1)
    def create_admin():
        username = f"admin"
        phone_number = f"+998889990011"
        admin = User.objects.create(username=username, phone_number=phone_number, password="qwerty1234", is_admin=True, is_staff=True)
        return admin    
    
    return create_admin

@pytest.fixture
def lesson(created_group, teacher_factory):
    # Create a test Lesson
    return Lesson.objects.create(
        group=created_group,
        unite='P1',
        vocabulary='P1V',
        grammar='P1G',
        home_work='P1H',
        date_created='2023-09-26'
    )