from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.db import models
from .models import Menu, MenuItem


def home(request, menu_url, item_urls=None):
  if not item_urls:
    current_url = request.path
    current_named_url = resolve(current_url).url_name if resolve(current_url).url_name else ''

    menus = get_matching_menus(menu_url, current_named_url)

    context = {
      'menu_url': menu_url,
      'menus': menus
    }

    return render(request, 'main.html', context)

  item_url = [item_url for item_url in item_urls.split('/') if item_url][-1]

  item = get_object_or_404(MenuItem, url=item_url)

  url_parts = []

  def add_parents(item):
    if item.parent:
      add_parents(item.parent)
    url_parts.append(str(item.id))


  add_parents(item)

  url_parts.insert(0, menu_url)

  final_url = '/' + '/'.join(url_parts)

  # return redirect(final_url)

  current_url = request.path
  current_named_url = resolve(current_url).url_name if resolve(current_url).url_name else ''

  # upd_current_url = current_url.strip('/')
  menus = get_matching_menus(menu_url, current_named_url)

  context = {
    'menu_url': menu_url,
    'item_url': item_url,
    'menus': menus
  }

  return render(request, 'main.html', context)


def get_matching_menus(current_url, current_named_url):
  return Menu.objects.filter(
    models.Q(url=current_url) | models.Q(named_url=current_named_url)
  )
