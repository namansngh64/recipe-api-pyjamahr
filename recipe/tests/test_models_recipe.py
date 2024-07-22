import pytest
from django.contrib.auth import get_user_model
from recipe.models import Recipe, RecipeCategory, RecipeLike

User = get_user_model()

@pytest.mark.django_db
def test_recipe_creation():
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
    assert recipe.title == 'Chocolate Cake'
    assert recipe.get_total_number_of_likes() == 0

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
    recipe_like = RecipeLike.objects.create(user=user, recipe=recipe)
    assert recipe.get_total_number_of_likes() == 1
