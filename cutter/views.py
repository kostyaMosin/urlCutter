from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cutter.forms import UrlSubmitForm
from cutter.models import ShortUrl, ClickShortUrl


def view_form(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'form': UrlSubmitForm()})
    elif request.method == 'POST':
        form = UrlSubmitForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            data = {'url': cd.get('url')}
            if custom_slug := cd.get('custom_slug'):
                data['slug'] = custom_slug
            short_url = ShortUrl.objects.create(**data)
            return render(request, 'success.html', {'short_url': short_url})
        return render(request, 'index.html', {'form': form})


def view_redirect_add_click(request, slug):
    if request.method == 'GET':
        short_url = get_object_or_404(ShortUrl, slug=slug)
        ClickShortUrl.objects.create(short_url=short_url)
        return redirect(short_url.url)


def view_short_urls_list(request):
    if request.method == 'GET':
        data = ShortUrl.objects.filter().order_by('-created_at')
        paginator = Paginator(data, 4)
        page = request.GET.get('page')

        try:
            short_urls = paginator.page(page)
        except PageNotAnInteger:
            short_urls = paginator.page(1)
        except EmptyPage:
            short_urls = paginator.page(paginator.num_pages)

        context = {
            'data': short_urls,
            'page': page,
        }
        return render(request, 'urls.html', context)
