from django import template
from django.core.exceptions import ObjectDoesNotExist
from menu.models import Menu, MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
  request = context['request']
  current_url = request.path

  try:
    menu = Menu.objects.get(name=menu_name)
  except ObjectDoesNotExist:
    return {'menu_tree': []}

  items = MenuItem.objects.filter(menu=menu).select_related('parent').order_by('parent', 'order')
  current_level = 0

  def build_tree(parent=None):
    tree = []
    for item in items:
      if item.parent == parent:
        tree.append({
          'item': item,
          'children': build_tree(item),
          'active': current_url == '/',
          'sub_active': False,
        })
    return tree

  return {'menu_tree': build_tree(), 'current_url': current_url, 'current_level': current_level + 1}


@register.inclusion_tag('menu/recursive_menu.html', takes_context=True)
def draw_submenu(context, node, current_level):
  node['sub_active'] = node['item'].url in context['current_url']
  node['active'] = context['current_url'].endswith(f'{node["item"].get_absolute_url()}/')
  node['item_url'] = transform_url(node, context['current_url'], current_level)
  return {
    'sub_tree': [node],
    'current_url': context['current_url'],
    'show_children': node['active'] or node['sub_active'],
    'current_level': current_level + 1
  }


def transform_url(node, absolute_path, current_level):
  path_parts = absolute_path.strip('/').split('/')
  upd_path = '/'
  total_levels = 0
  if current_level == 1:
    return f'/{node["item"].url}/'
  for part in path_parts:
    if total_levels == current_level:
      upd_path += node['item'].url
      break
    total_levels += 1
    if part != node['item'].url:
      upd_path += f'{part}/'
    else:
      upd_path += node['item'].url
      break
  if node['item'].url not in upd_path:
    return node['item'].get_absolute_url()
  return upd_path
