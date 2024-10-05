from typing import List, Optional
from django.shortcuts import render
from django.db.models import Prefetch, Q
from django.http import HttpResponse, HttpRequest
from .models import Menu, MenuItem


def tree_menu(request: HttpRequest, item_url: str) -> HttpResponse:
  """
  Построение списка меню на странице с опр. url
  """
  current_url = request.path.strip('/')

  menus = get_matching_menus(current_url)

  context = {
    'item_url': item_url,
    'menus': menus
  }

  return render(request, 'tree_menu.html', context)


def main(request: HttpRequest) -> HttpResponse:
  """
  Отображение всех меню на главной странице у которых есть либо url, либо named url
  """
  menus = Menu.objects.filter(
    Q(url__isnull=False) & ~Q(url='') |
    Q(named_url__isnull=False) & ~Q(named_url='')
  )
  return render(request, 'main.html', {'menus': menus})


def get_matching_menus(current_url: str) -> Optional[List[Menu]]:
  """
  Поиск меню по url, для отображения на одной странице
  """
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
