from django import template
from django.db.models import Prefetch
from menu.models import Menu, MenuItem
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_url, menu_name, item_url=None):

    try:
        menu = Menu.objects.prefetch_related(
            Prefetch('items', queryset=MenuItem.objects.select_related('parent'))
        ).get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    # Функция для рекурсивного создания полного URL для элемента меню
    def build_full_url(item):
        if item.parent:
            return build_full_url(item.parent) + '/' + item.get_url()
        return f'/{menu_url}/' + item.get_url()

    # Рекурсивная функция для отображения меню
    def render_menu(items, parent=None):
        html = '<ul>'
        for item in items:
            if item.parent == parent:
                full_url = build_full_url(item)
                css_class = 'active' if item.get_url() == item_url else ''
                html += f'<li><a class="{css_class}" href="{full_url}">{item.title}</a>'
                html += render_menu(items, item)
                html += '</li>'
        html += '</ul>'
        return html

    # Генерируем HTML для всего меню
    menu_html = render_menu(menu.items.all())
    return mark_safe(menu_html)