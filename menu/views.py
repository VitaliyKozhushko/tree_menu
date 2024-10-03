from django.shortcuts import render
from .models import Menu


def home(request, path=''):
  menu = list(Menu.objects.values_list('name', flat=True))
  return render(request, 'main.html', {'current_url': request.path, 'menu_list': menu})
