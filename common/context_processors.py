from django.conf import settings
from django.contrib.sites.models import get_current_site


def meta_data(request):
    meta = dict()
    meta['site_name'] = settings.SITE_NAME
    meta['site_url'] = ''.join(['http://', get_current_site(None).domain])
    meta['site_title'] = settings.SITE_TITLE
    meta['site_domain'] = get_current_site(None).domain
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
    options['DEFAULT_AVATAR'] = settings.DEFAULT_AVATAR
    options['JS_VERSION'] = settings.JS_VERSION
    options['CSS_VERSION'] = settings.CSS_VERSION
    options['FOOTER_TEXT'] = settings.FOOTER_TEXT
    options['FOOTER_COPY_RIGHT'] = settings.FOOTER_COPY_RIGHT
    options['NUMBER_OF_TAGS'] = settings.NUMBER_OF_TAGS
    options['SITE_URL'] = ''.join(['http://', get_current_site(None).domain])
    options['SITE_TWITTER_URL'] = settings.SOCIAL_LINKS['twitter'].format(title=settings.SITE_TITLE, url=options['SITE_URL'])
    options['SITE_GOOGLEPLUS_URL'] = settings.SOCIAL_LINKS['googleplus'].format(url=options['SITE_URL'])
    options['SITE_FACEBOOK_URL'] = settings.SOCIAL_LINKS['facebook'].format(url=options['SITE_URL'], title=settings.SITE_TITLE)

    return {'options': options}
