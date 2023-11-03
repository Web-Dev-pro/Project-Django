import pytest
from apps.authentication.models import Group
from rest_framework.test import APIClient
from apps.authentication.models import (
    Student,
    Group,
    User,
    Mark,
    Lesson,
    Parent,
    StudentProfile,
    Teacher,
    TeacherProfile
)
from rest_framework import status
from django.urls import reverse
from mixer.backend.django import mixer
from django.test import RequestFactory
from rest_framework.request import Request
import datetime
import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_create_student_registration_success(created_group):
    """
    client -- get api client to make post, get, update and delete operations
    url -- reverse url for ongoing view address
    payload -- data to be created as for student, user model accordingly
    response -- paste url, payload with client post request
    last check created student and users info match
    """
    client = APIClient()
    url = reverse('student_register')
    payload = {
        "username": "John",
        "password1": "testpassoword",
        "password2": "testpassoword",
        "full_name": "John Doe",
        "age": 34,
        "user": {
            "phone_number": "+998904447799",
        },
        "group_name": created_group.name
    }

    response = client.post(url, data=payload, format='json', follow=True)
    assert response.status_code == status.HTTP_201_CREATED

    # verify created student is available
    student = Student.objects.filter(user__username='John').first()
    assert student is not None
    assert student.full_name == 'John Doe'
    assert student.age == 34
    assert student.group == created_group

    # verify that correct user linked to newly created student
    user = User.objects.filter(username='John').first()
    assert user is not None
    assert user.phone_number == '+998904447799'
    assert user.user_unique_id == user.user_unique_id
    assert user.is_student == True
    # pytest.skip("Skipping student registration test") 

@pytest.mark.django_db
def test_create_teacher_registration_success():
    client = APIClient()
    url = reverse('teacher_register')
    payload = {
        "username": "testteacher",
        "password1": "testpassword",
        "password2": "testpassword",
        "user": {
            "phone_number": "+998904441189"
        },
        "full_name": "Teacher Olimov"
    }
    response = client.post(url, data=payload, format='json', follow=True)
    assert response.status_code == status.HTTP_201_CREATED
    # pytest.skip("skipping teacher creation test...")

@pytest.mark.django_db
def test_get_average_mark_without_marks(student_factory):
    student = student_factory()
    assert student.get_average_mark() == 0
    # pytest.skip("skipping average mark without marks...")

@pytest.mark.django_db
def test_get_average_mark_with_marks(student_factory, group_factory, mark_factory, lesson):
    group = group_factory()
    student = student_factory()
    mark1 = mark_factory(student=student, lesson=lesson, mark=80)
    mark2 = mark_factory(student=student, lesson=lesson, mark=90)
    assert student.get_average_mark() == pytest.approx(85.0)
    response = student.get_average_mark() == pytest.approx(87)
    assert response == False    
    # pytest.skip("skipping average mark with marks...")


# test parent registration
@pytest.mark.django_db
def test_parent_registration(student_factory):
    # logger.info("Test is success of creation parent")
    student = student_factory()
    parent = mixer.blend(Parent, student=student)
    assert parent.student == student
    # pytest.skip("creation of parent test is skipping...")

@pytest.mark.django_db
def test_student_profile_creation(student_factory):
    student = student_factory()
    profile = student.student_profile

    assert isinstance(profile, StudentProfile)
    assert profile.user == student
    # pytest.skip("creation of student profile test is skipping...")


@pytest.mark.django_db
def test_teacher_profile_creation(teacher_factory):
    teacher = teacher_factory()
    profile = teacher.teacher_profile

    # assert teacher has profile that is linked or instance of profile
    assert isinstance(profile, TeacherProfile)
    assert profile.user == teacher
    # pytest.skip("creation of teacher profile test is skipping...")