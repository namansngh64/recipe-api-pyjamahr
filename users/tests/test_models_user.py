import pytest
from django.contrib.auth import get_user_model
from users.models import Profile
from recipe.models import Recipe

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'

@pytest.mark.django_db
def test_profile_creation():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    profile = Profile.objects.create(user=user)
    assert profile.user == user

@pytest.mark.django_db
def test_bookmark_recipe():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password@123')
    profile = Profile.objects.create(user=user)
    recipe = Recipe.objects.create(title='Test Recipe', author=user, cook_time=30)
    profile.bookmarks.add(recipe)
    assert recipe in profile.bookmarks.all()
