import pytest
from apps.authentication.models import (
    User,
    Lesson,
    Parent,
    Student
)
from apps.comment.models import StudentCommentFromTeacher
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status
from mixer.backend.django import mixer
import logging

logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_comment_creation_test_from_teacher_to_student(api_client,
                                                       lesson,
                                                       teacher_factory,
                                                       student_factory,):
    """
    creation of test by teacher to student and endpoint availability
    finding a bug
    """
    
    # authenticate user
    teacher = teacher_factory()
    # get student id
    student = student_factory()
    # get request from url
    url = reverse("student-comment", kwargs={"student_id": student.id, "lesson_id": lesson.id})
    data = {
        "comment": "He is great student",
        "teacher": teacher.id,
        "student": student.id,
        "lesson": lesson.id
    }
    api_client.force_authenticate(user=teacher.user)
    response = api_client.post(url, data)
    
    # assert status
    assert response.status_code == status.HTTP_201_CREATED
    # assert response data
    assert response.data['comment'] == "He is great student"
    assert response.data['teacher'] == teacher.id
    assert response.data['student'] == student.id
    assert response.data['lesson'] == lesson.id
    # assert comment existance 
    assert StudentCommentFromTeacher.objects.exists()
    
    comment_id = response.data["id"]

    return comment_id
    
@pytest.mark.django_db
def test_comment_reply_from_parent_to_teacher(api_client,
                                              parent_factory,
                                              lesson,
                                              teacher_factory,
                                              student_factory):
    """
    creation of comment from parent to teachers. Should be validate of comment reply and its endpoint
    """
    
    # authenticate user as parent
    parent = parent_factory() 
    # get comment id
    # we create second student_factory_reply as it is required to avoid UNIQUE Cons.. problem occuring.
    # Because two user is being created in two class with same phone_number, password etc.
    # So creating along second student with different credentials prevents double creation of student
    
    comment_id = test_comment_creation_test_from_teacher_to_student(
        api_client,
        lesson,
        teacher_factory,
        student_factory)

    url = reverse("reply_to_teacher_from_parent", kwargs={"comment_id": comment_id})
    data = {
        "comment": comment_id,
        "parent": parent.id,
        "reply": "Yeah thank you for your comment for my child"
    }
    
    # Force Authentication should placed at the end after urls and data. Setting it in top
    # of the class authenticates before response comes in 
    api_client.force_authenticate(user=parent.user)
    response = api_client.post(url, data)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['comment'] == comment_id
    assert response.data['parent'] == parent.id
    assert response.data['reply'] == "Yeah thank you for your comment for my child"
    
@pytest.mark.django_db
def test_comment_delete_comes_from_teacher(api_client,
                                           lesson,
                                           admin_factory,
                                           teacher_factory,
                                           student_factory):
    """
    test comment delete, check endpoints
    """
    admin = admin_factory()
    student = student_factory()
    teacher = teacher_factory()
    data = {
        "id": 2,
        "teacher": teacher.id,
        "student": student.id,
        "lesson": lesson.id,
        "comment": "He is great student"
    }
    url_post = reverse("student-comment", kwargs={"student_id": student.id, "lesson_id": lesson.id})
    url_del = reverse('comment-delete', kwargs={"pk": data['id']})
    api_client.force_authenticate(user=teacher.user)
    response_post = api_client.post(url_post, data)
    response_del = api_client.delete(url_del)
    # assert
    assert response_post.status_code == status.HTTP_201_CREATED
    assert response_del.status_code == status.HTTP_204_NO_CONTENT
    
    
    

    
    