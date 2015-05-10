from django.conf import settings


def meta_data(request):
    meta = dict()
    meta['site_name'] = settings.SITE_NAME
    meta['site_url'] = settings.SITE_URL
    meta['site_db_admins'] = settings.SITE_FB_ADMINS
    meta['site_bitly_verification'] = settings.SITE_BITLY_VERIFICATION
    meta['accept_gzip'] = 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', '')
    return {'meta': meta}
