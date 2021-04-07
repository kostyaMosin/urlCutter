from django.urls import path

from .views import view_short_urls_list, view_form, view_redirect_add_click

urlpatterns = [
    path('', view_form, name='form'),
    path('urls', view_short_urls_list, name='urls'),
    path('<slug>', view_redirect_add_click, name='redirect'),
]
