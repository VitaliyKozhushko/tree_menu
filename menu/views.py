from django.shortcuts import render
from django.urls import resolve
from django.db import models
from .models import Menu


def home(request, path=''):
  current_url = request.path
  current_named_url = resolve(current_url).url_name if resolve(current_url).url_name else None

  menus = Menu.objects.filter(
    (models.Q(url=current_url) | models.Q(named_url=current_named_url)) &
    (models.Q(url__isnull=False) | models.Q(named_url__isnull=False))
  )

  print(menus)

  return render(request, 'main.html', {'menus': menus})
