from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from recipesAPI.models import Recipe, UserProfile


@receiver(post_save, sender=Recipe)
def handle_recipe_slug(sender, instance, created, *args, **kwargs):
    lower_title = instance.title.lower()
    slug = slugify(f'{lower_title}-{instance.id}')

    if created or slug != instance.slug:
        instance.slug = slugify(f'{lower_title}-{instance.id}')
        instance.save()
