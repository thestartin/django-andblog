from django.conf import settings
from django.core.cache import cache

from pages.models import Page


def set_menu_cache():
    """
    Method to set Menu cache
    :return:
    """
    menu_items = []
    menu_items.extend([(item, False, link) for item, link in settings.STATIC_MENU_ITEMS.items()])
    for item in Page.objects.all()[:settings.MAX_MENU_ITEMS-len(menu_items)]:
        menu_items.append((item.menu_display_name, True, item.menu_name))

    cache.set('menu', menu_items)
