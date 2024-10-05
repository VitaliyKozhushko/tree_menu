from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def menu_link(menu):
    if menu.url:
        return reverse('tree_menu', kwargs={'item_url': menu.url})
    return reverse('tree_menu', kwargs={'item_url': menu.named_url})
