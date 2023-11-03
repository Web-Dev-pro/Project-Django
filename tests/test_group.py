from apps.authentication.models import Group
from rest_framework import status
from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_group_api_data_get(api_client, admin_factory):
    """_summary_

    Args:
        api_client (_general_): _To get response from url address needed api client get method_
        admin_factory (_auth_): _To authenticate user as to get data of gorup_
    """
    url = reverse("group-general")
    user = admin_factory()
    api_client.force_authenticate(user=user) # authenticate user as admin
    response = api_client.get(url)
    # assert data
    assert response.status_code == status.HTTP_200_OK
    
@pytest.mark.django_db
def test_group_api_data_post(api_client, admin_factory, teacher_factory):
    """_summary_

    Args:
        api_client (_general_): _To get response from url address needed api client get method_
        admin_factory (_auth_): _To authenticate user as to get data of gorup_
    """ 
    teacher = teacher_factory()
    url = reverse("group-general")
    user = admin_factory()
    api_client.force_authenticate(user=user) # authenticate user as admin
    data = {
        "name": "A3",
        "course_date": "2022-08-09",
        "total_courses": 30,
        "course_time": "12:30",
        "teacher": teacher.id,
        "days": "Mon, Wed, Fri",
    }
    response = api_client.post(url, data)
    # assert data
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'A3'
    assert response.data['course_date'] == "2022-08-09"
    assert response.data['total_courses'] == 30
    assert response.data['course_time'] == "12:30"
    assert response.data['teacher'] == teacher.id
    assert response.data['days'] == "Mon, Wed, Fri"