from django import template
from django.db.models import Prefetch
from ..models import Menu, MenuItem
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_id, item_url):
  request = context['request']
  current_url = request.path.strip('/')
  try:
    menu = Menu.objects.prefetch_related(
      Prefetch(
        'items',
        queryset=MenuItem.objects.all().select_related('parent').prefetch_related('children')
      )
    ).get(id=menu_id)
    print('menu_id:', menu_id)
  except Menu.DoesNotExist:
    return ''

  # Функция для поиска активного элемента и его родительской цепочки
  def find_active_item_and_parents(items, current_url):
    for item in items:
      full_url = item.get_url()
      if full_url == current_url:
        return item, [item] + list(find_all_parents(item))
    return None, []

  # Функция для получения всех родителей активного элемента
  def find_all_parents(item):
    if item.parent:
      return [item.parent] + find_all_parents(item.parent)
    return []

  active_item, active_parents = find_active_item_and_parents(menu.items.all(), current_url)

  # Рекурсивная функция для отображения меню
  def render_menu(items, parent=None, level=0):
    html = '<ul>'
    for item in items:
      if item.parent == parent:
        full_url = item.get_url()
        css_class = 'active' if item.get_url() == item_url else ''
        is_open = item in active_parents or item == active_item
        print('item:', item.title, full_url)
        if is_open or (active_item and active_item.parent == item):
            html += f'<li><a class="{css_class}" href="/{full_url}">{item.title}</a>'
            html += render_menu(items, item, level + 1)
            html += '</li>'
        else:
            html += f'<li><a class="{css_class}" href="/{full_url}">{item.title}</a></li>'
    html += '</ul>'
    return html

  # Генерируем HTML для всего меню
  menu_html = render_menu(menu.items.all())
  return mark_safe(menu_html)
