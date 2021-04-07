from django.db import models

from .slug import generate_slug


class ShortUrl(models.Model):
    url = models.URLField(unique=True)
    slug = models.CharField(
        max_length=15,
        primary_key=True,
        default=generate_slug(),
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ClickShortUrl(models.Model):
    short_url = models.ForeignKey(
        ShortUrl,
        null=True,
        on_delete=models.CASCADE,
        related_name='clicks',
    )
    created_at = models.DateTimeField(auto_now_add=True)

