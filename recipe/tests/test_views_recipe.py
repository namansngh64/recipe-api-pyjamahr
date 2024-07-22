import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory

User = get_user_model()

@pytest.mark.django_db
def test_recipe_list():
    client = APIClient()
    url = reverse('recipe:recipe-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_recipe_create():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('recipe:recipe-create')
    category = RecipeCategory.objects.create(name='Dessert')
    data = {
        'title': 'Chocolate Cake',
        'desc': 'Delicious chocolate cake',
        'cook_time': '00:30:00',
        'ingredients': 'Chocolate, Flour, Sugar, Eggs',
        'procedure': 'Mix and bake',
        'category': {'id': category.id, 'name': 'Dessert'},
        'picture': 'path/to/picture.jpg'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_recipe_detail():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    category = RecipeCategory.objects.create(name='Dessert')
    recipe = Recipe.objects.create(
        author=user,
        category=category,
        picture='path/to/picture.jpg',
        title='Chocolate Cake',
        desc='Delicious chocolate cake',
        cook_time='00:30:00',
        ingredients='Chocolate, Flour, Sugar, Eggs',
        procedure='Mix and bake'
    )
    client = APIClient()
    url = reverse('recipe:recipe-detail', args=[recipe.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Chocolate Cake'

@pytest.mark.django_db
def test_recipe_like():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    category = RecipeCategory.objects.create(name='Dessert')
    recipe = Recipe.objects.create(
        author=user,
        category=category,
        picture='path/to/picture.jpg',
        title='Chocolate Cake',
        desc='Delicious chocolate cake',
        cook_time='00:30:00',
        ingredients='Chocolate, Flour, Sugar, Eggs',
        procedure='Mix and bake'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('recipe:recipe-like', args=[recipe.id])
    response = client.post(url)
    assert response.status_code == status.HTTP_201_CREATED
