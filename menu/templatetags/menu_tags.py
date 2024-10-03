from django import template
from django.db.models import Prefetch
from menu.models import Menu, MenuItem
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    try:
        menu = Menu.objects.prefetch_related(
            Prefetch('items', queryset=MenuItem.objects.select_related('parent'))
        ).get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    # Выделение активного пункта и его родителей
    def find_active_item(items, current_url):
        for item in items:
            if item.get_url() == current_url:
                return item
            if item.children.count() > 0:
                active_child = find_active_item(item.children.all(), current_url)
                if active_child:
                    return active_child
        return None

    active_item = find_active_item(menu.items.all(), current_url)

    def render_menu(items, parent=None):
        html = '<ul>'
        for item in items:
            if item.parent == parent:
                css_class = 'active' if item == active_item else ''
                html += f'<li class="{css_class}"><a href="{item.get_url()}">{item.title}</a>'
                html += render_menu(items, item)
                html += '</li>'
        html += '</ul>'
        return html

    menu_html = render_menu(menu.items.all())
    return mark_safe(menu_html)
