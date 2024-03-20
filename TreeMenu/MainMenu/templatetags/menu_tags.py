from django import template
from MainMenu.models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    all_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    current_url = request.path
    
    def build_menu(items, parent=None, current_url=None, active_path=None):
        menu = []
        for item in items:
            if item.parent == parent:
                is_active = item.get_absolute_url() == current_url
                if active_path and not is_active:
                    is_open = item in active_path
                else:
                    is_open = is_active
                children = build_menu(items, parent=item, current_url=current_url, active_path=active_path)
                menu.append({'item': item, 'children': children, 'is_active': is_active, 'is_open': is_open})
        return menu

    # Find the active path
    active_path = []
    for item in all_items:
        if item.get_absolute_url() == current_url:
            active_path = get_active_path(item)
            break

    menu_tree = build_menu(all_items, current_url=current_url, active_path=active_path)
    return {'menu_tree': menu_tree}

def get_active_path(item):
    path = []
    parent = item.parent
    while parent is not None:
        path.append(parent)
        parent = parent.parent
    return path[::-1]