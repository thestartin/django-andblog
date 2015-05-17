from django.conf import settings
from django.contrib.sites.models import get_current_site


def meta_data(request):
    meta = dict()
    meta['site_name'] = settings.SITE_NAME
    meta['site_url'] = settings.SITE_URL
    meta['site_db_admins'] = settings.SITE_FB_ADMINS
    meta['site_bitly_verification'] = settings.SITE_BITLY_VERIFICATION
    meta['DEBUG'] = settings.DEBUG
    meta['accept_gzip'] = 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', '')
    return {'meta': meta}


def settings_flags(request):
    options = dict()
    options['ENABLE_DISQUS'] = settings.ENABLE_DISQUS
    #options['LOGO_URL'] = ''.join(['http://', get_current_site(None).domain, settings.LOGO_URL])
    options['LOGO_URL'] = settings.LOGO_URL
    options['JS_VERSION'] = settings.JS_VERSION
    options['CSS_VERSION'] = settings.CSS_VERSION
    return {'options': options}
