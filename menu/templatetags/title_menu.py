from django import template
from django.urls import reverse
from ..models import Menu

register = template.Library()


@register.simple_tag
def menu_link(menu: Menu) -> str:
  """
  Определение отображения правильной ссылки на меню на главной странице
  """
  if menu.url:
    return reverse('tree_menu', kwargs={'item_url': menu.url})
  return reverse('tree_menu', kwargs={'item_url': menu.named_url})
