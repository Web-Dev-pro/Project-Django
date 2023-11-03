import pytest
from apps.authentication.models import Lesson, User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from mixer.backend.django import mixer

@pytest.mark.django_db
def test_list_of_lessons_api(api_client, lesson, admin_factory):
    """
    test all lesson availability and endpoint response
    """
    # get request
    url = reverse('lesson-general')
    # authenticate user
    admin = admin_factory()
    api_client.force_authenticate(user=admin)
    response = api_client.get(url)
    # assert that response is ok with 200
    assert response.status_code == status.HTTP_200_OK

    # assert response data
    assert response.data[0]['unite'] == "P1"
    assert response.data[0]['vocabulary'] == "P1V"
    assert response.data[0]['grammar'] == "P1G"
    assert response.data[0]['home_work'] == "P1H"
    # assert response.data[0]['date_created'] == "2023-09-26" to avoid time problem
    # pytest.skip("test all lessons endpoints skipping...")

@pytest.mark.django_db
def test_retrieve_lesson_api(api_client, lesson, admin_factory):
    """
    test single lesson retrieve and endpoint response
    """
    
    # get request
    url = reverse('lesson-detail', kwargs={'pk': lesson.pk})
    # authenticate user
    admin = admin_factory()
    api_client.force_authenticate(user=admin)
    response = api_client.get(url)
    # assert response status
    assert response.status_code == status.HTTP_200_OK

    # assert response data
    assert response.data['unite'] == "P1"
    assert response.data['vocabulary'] == "P1V"
    assert response.data['grammar'] == "P1G"
    assert response.data['home_work'] == "P1H"
    # assert response.data['date_created'] == "2023-09-26" to avoid time problem
    # pytest.skip("test single lesson retrieve endpoint skipping...")


@pytest.mark.django_db
def test_create_lesson_api(api_client, admin_factory, group_factory):
    """
    test lesson creation and endpoint response
    """
    
    group = group_factory()
    # get request
    url = reverse("lesson-create", kwargs={"pk": group.pk})
    data = {
        'unite': 'Test Unite',
        'vocabulary': 'Test Vocabulary',
        'grammar': 'Test Grammar',
        'home_work': 'Test Homework',
        'date_created': '2023-09-26'
    }
    # authenticate user
    admin = admin_factory()
    api_client.force_authenticate(user=admin)
    response = api_client.post(url, data) 
    # assert response status to ensure returning 201 created
    assert response.status_code == status.HTTP_201_CREATED
    # assert lesson in exists in database
    assert Lesson.objects.exists()
    # get created lesson first
    created_lesson = Lesson.objects.first()
    # assert created lesson is linked with group pk
    assert created_lesson.group == group
    # pytest.skip("test of create lesson is skipping...")

@pytest.mark.django_db
def test_delete_lesson(api_client, admin_factory, lesson):
    """
    test lesson deletion and endpoint response
    """
    
    # get request
    url = reverse("lesson-delete", kwargs={"pk": lesson.pk})
    # authenticate user
    admin = admin_factory()
    api_client.force_authenticate(user=admin)
    response = api_client.delete(url)
    # assert data is being deleted
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # pytest.skip("test of deletion lesson is skipping")