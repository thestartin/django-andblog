from django.core.cache import cache

from common.funcs import set_menu_cache


def menu(request):
    menu_items = cache.get('menu')
    if not menu_items:
        set_menu_cache()
    menu_items = cache.get('menu')
    return {'menu': menu_items}
