from django.conf import settings
from django.core.cache import cache

from .models import Page


def menu(request):
    menu_items = cache.get('menu')
    if not menu_items:
        menu_items = []
        menu_items.extend([(item, False) for item in settings.STATIC_MENU_ITEMS])
        for item in Page.objects.all()[:settings.MAX_MENU_ITEMS-len(menu_items)]:
            menu_items.append((item.menu_name, True))

        cache.set('menu', menu_items)

    return {'menu': menu_items}
