from django.contrib import admin

from .models import ShortUrl, ClickShortUrl


admin.site.register(ShortUrl)
admin.site.register(ClickShortUrl)
