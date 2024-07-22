import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from recipe.models import Recipe
from users.models import Profile

User = get_user_model()
client = APIClient()

@pytest.mark.django_db
def test_user_registration():
    url = reverse('users:create-user')
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password@123'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'tokens' in response.data

@pytest.mark.django_db
def test_user_login():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    url = reverse('users:login-user')
    data = {'email': 'test@example.com', 'password': 'password123'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'tokens' in response.data

@pytest.mark.django_db
def test_user_logout():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    refresh_token = str(RefreshToken.for_user(user))
    client.force_authenticate(user=user)
    url = reverse('users:logout-user')
    data = {'refresh': refresh_token}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_205_RESET_CONTENT

@pytest.mark.django_db
def test_user_profile():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    Profile.objects.create(user=user)
    client.force_authenticate(user=user)
    url = reverse('users:user-profile')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['user'] == user.id

@pytest.mark.django_db
def test_user_avatar():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    profile = Profile.objects.create(user=user)
    client.force_authenticate(user=user)
    url = reverse('users:user-avatar')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['user'] == profile.user.id

@pytest.mark.django_db
def test_user_bookmarks():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    profile = Profile.objects.create(user=user)
    recipe = Recipe.objects.create(title='Test Recipe', author=user, cook_time=30)
    client.force_authenticate(user=user)
    url = reverse('users:user-bookmark', kwargs={'pk': user.id})
    response = client.post(url, {'id': recipe.id}, format='json')
    assert response.status_code == status.HTTP_200_OK
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['id'] == recipe.id
    response = client.delete(url, {'id': recipe.id}, format='json')
    assert response.status_code == status.HTTP_200_OK
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
