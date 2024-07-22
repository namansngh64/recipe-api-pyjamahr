# recipe/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Recipe

@shared_task
def send_email_notification_to_author(recipe_id, user_email):
    """
    Send an email notification to the author of the recipe about new likes.
    """
    # Fetch the recipe
    recipe = Recipe.objects.get(id=recipe_id)

    subject = f"Your recipe '{recipe.title}' has received new likes!"
    message = f"Hello,\n\nYour recipe '{recipe.title}' has received new likes. Check it out on our platform!"
    from_email = 'no-reply@test.com'

    send_mail(subject, message, from_email, [user_email])
    
@shared_task
def send_daily_likes_summary():
    """
    Send a daily summary of likes to all recipe authors.
    """
    yesterday = now() - timedelta(days=1)
    # Fetch all recipes
    recipes = Recipe.objects.all()
    
    for recipe in recipes:
        today_likes = recipe.recipelike_set.filter(created=yesterday.date()).count()
        if today_likes > 0:
            send_email_notification_to_author.delay(recipe.id, recipe.author.email)
