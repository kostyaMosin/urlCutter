from django.core.paginator import Page
from django.test import TestCase

from cutter.forms import UrlSubmitForm
from cutter.models import ShortUrl


class ViewTestCase(TestCase):
    def test_view_form_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, UrlSubmitForm)

    def test_view_form_post(self):
        url = 'https://google.com'
        response = self.client.post('/', {'url': url})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertIn('short_url', response.context)
        short_url = response.context['short_url']
        self.assertIsInstance(short_url, ShortUrl)
        self.assertEqual(url, short_url.url)
        self.assertEqual(short_url.clicks.count(), 0)

    def test_view_form_post_with_custom_slug(self):
        url = 'https://google.com'
        custom_slug = 'sQ2e3'
        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertIn('short_url', response.context)
        short_url = response.context['short_url']
        self.assertIsInstance(short_url, ShortUrl)
        self.assertEqual(url, short_url.url)
        self.assertEqual(short_url.clicks.count(), 0)
        self.assertEqual(short_url.slug, custom_slug)

    def test_view_form_post_with_custom_slug_not_unique(self):
        url = 'https://google.com'
        custom_slug = 'sQ2e3'

        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertIn('short_url', response.context)
        short_url = response.context['short_url']
        self.assertIsInstance(short_url, ShortUrl)
        self.assertEqual(url, short_url.url)
        self.assertEqual(short_url.clicks.count(), 0)
        self.assertEqual(short_url.slug, custom_slug)

        url = 'https://google.com/sD32xa'
        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFormError(response, 'form', 'custom_slug', 'This slug is already taken')
        self.assertNotIn('short_url', response.context)

    def test_view_form_post_with_url_not_unique(self):
        url = 'https://google.com'
        custom_slug = 'sQ2e3'

        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
        self.assertIn('short_url', response.context)
        short_url = response.context['short_url']
        self.assertIsInstance(short_url, ShortUrl)
        self.assertEqual(url, short_url.url)
        self.assertEqual(short_url.clicks.count(), 0)
        self.assertEqual(short_url.slug, custom_slug)

        custom_slug = 'kmE32a'
        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFormError(response, 'form', 'url', 'This url is already taken')
        self.assertNotIn('short_url', response.context)

    def test_view_form_post_with_custom_slug_long(self):
        url = 'https://google.com'
        custom_slug = 'sQ2e3sQ2e3sQ2e3sQ2e3'
        response = self.client.post('/', {'url': url, 'custom_slug': custom_slug})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFormError(
            response, 'form', 'custom_slug', 'Ensure this value has at most 15 characters (it has 20).')
        self.assertNotIn('short_url', response.context)

    def test_view_redirect_add_click(self):
        url = 'https://google.com'
        short_url = ShortUrl.objects.create(url=url)
        self.assertEqual(short_url.clicks.count(), 0)

        response = self.client.get(f'/{short_url.slug}')
        self.assertRedirects(response, url, 302, fetch_redirect_response=False)

        short_url = ShortUrl.objects.get(slug=short_url.slug)
        self.assertEqual(short_url.clicks.count(), 1)

    def test_view_redirect_404(self):
        response = self.client.get('/failure')
        self.assertEqual(response.status_code, 404)

    def test_view_short_urls_list(self):
        response = self.client.get('/urls')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'urls.html')
        self.assertIn('data', response.context)
        data = response.context['data']
        self.assertIsInstance(data, Page)
