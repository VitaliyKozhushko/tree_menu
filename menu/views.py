from django.shortcuts import render
from django.urls import resolve
from django.db import models
from .models import Menu


def home(request, path=''):
  current_url = request.path
  current_named_url = resolve(current_url).url_name if resolve(current_url).url_name else ''

  upd_current_url = current_url.strip('/')
  print(upd_current_url)
  menus = get_matching_menus(upd_current_url, current_named_url)

  return render(request, 'main.html', {'menus': menus})


def get_matching_menus(current_url, current_named_url):
  return Menu.objects.filter(
    models.Q(url=current_url) | models.Q(named_url=current_named_url)
  )
