from django.db.models.signals import post_save
from django.dispatch import receiver

from recipesAPI.models import Recipe


@receiver(post_save, sender=Recipe)
def handle_recipe_slug(sender, instance, created, *args, **kwargs):
    current_slug = f'{instance.title}-{instance.id}'
    if created or current_slug != instance.slug:
        instance.slug = f'{instance.title}-{instance.id}'
        instance.save()
