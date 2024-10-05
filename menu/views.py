from http.client import HTTPException

from django.shortcuts import render, get_object_or_404
from django.urls import resolve
from .models import Menu, MenuItem
from django.db.models import Prefetch, Q
from django.http import HttpResponse, HttpResponseNotFound


def tree_menu(request, item_url):
  current_url = request.path.strip('/')

  menus = get_matching_menus(current_url)

  context = {
    'item_url': item_url,
    'menus': menus
  }

  return render(request, 'tree_menu.html', context)

  # item_url = [item_url for item_url in item_urls.split('/') if item_url][-1]
  #
  # item = get_object_or_404(MenuItem, url=item_url, menu__url=menu_url)
  #
  # url_parts = []
  #
  # def add_parents(item):
  #   if item.parent:
  #     add_parents(item.parent)
  #   url_parts.append(str(item.id))
  #
  # add_parents(item)
  #
  # url_parts.insert(0, menu_url)
  #
  # current_url = request.path
  # current_named_url = resolve(current_url).url_name if resolve(current_url).url_name else ''
  #
  # menus = get_matching_menus(menu_url, current_named_url)
  #
  # context = {
  #   'menu_url': menu_url,
  #   'item_url': item_url,
  #   'menus': menus
  # }

  # return render(request, 'tree_menu.html', context)


def main(request):
  menus = Menu.objects.filter(
    Q(url__isnull=False) & ~Q(url='') |
    Q(named_url__isnull=False) & ~Q(named_url='')
  )
  return render(request, 'main.html', {'menus': menus})


def get_matching_menus(current_url):
  # Попытка найти меню или пункт меню по URL
  menu_with_items = Menu.objects.prefetch_related(
    Prefetch(
      'items',
      queryset=MenuItem.objects.select_related('menu').order_by('order')
    )
  ).filter(
    Q(url=current_url) |
    Q(items__url=current_url) |
    Q(named_url=current_url) |
    Q(items__named_url=current_url)
  ).distinct()

  if menu_with_items:
    return menu_with_items

  return None


def hello(request, menu_url):
  return HttpResponse('Hello world!')
