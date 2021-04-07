from django import forms

from cutter.models import ShortUrl
from cutter.slug import generate_slug


class UrlSubmitForm(forms.Form):
    url = forms.URLField(label='Url to be cut')
    custom_slug = forms.CharField(label='Custom slug', max_length=15, required=False)

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url:
            return

        if ShortUrl.objects.filter(url=url).exists():
            raise forms.ValidationError(f'{url} is already taken')
        return url

    def clean_custom_slug(self):
        custom_slug = self.cleaned_data['custom_slug']
        if not custom_slug:
            custom_slug = generate_slug()
            return custom_slug

        try:
            if ShortUrl.objects.filter(slug=custom_slug).exists():
                raise forms.ValidationError(f'{custom_slug} is already taken')
        except OverflowError:
            raise forms.ValidationError('Custom slug is too long')
        return custom_slug
