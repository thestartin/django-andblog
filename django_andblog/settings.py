"""
Django settings for django_andblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from collections import OrderedDict

from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm2hm(=+w=$=(di=zhxeo4mr+l%jbl05-cp1oc2r53do#^#uw*r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'sorl.thumbnail',
    'taggit',
    'crispy_forms',
    'rest_framework',
    'disqus',
    'redis_cache',
    'social.apps.django_app.default',
    'ckeditor',
    'common',
    'blog',
    'pages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.HttpBadReponseMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.google.GooglePlusAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
    'common.backends.EmailModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'pages.context_processors.menu',
    'common.context_processors.meta_data'
)

ROOT_URLCONF = 'django_andblog.urls'

WSGI_APPLICATION = 'django_andblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'andblog'),
        'USER': os.environ.get('DB_USER_NAME', 'andblog'),
        'PASSWORD': os.environ.get('DB_USER_PASSWORD', 'andblog')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'django_andblog/static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'django_andblog/assets/'),
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, 'blog/templates/')),
    os.path.abspath(os.path.join(BASE_DIR, 'blog/templates/includes')),
    os.path.abspath(os.path.join(BASE_DIR, 'common/templates/')),
    os.path.abspath(os.path.join(BASE_DIR, 'common/templates/includes')),
    os.path.abspath(os.path.join(BASE_DIR, 'django_andblog/templates/')),
    os.path.abspath(os.path.join(BASE_DIR, 'django_andblog/templates/includes')),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# Thumbnails
MEDIA_ROOT = UPLOAD_TO = os.path.join(BASE_DIR, 'django_andblog', 'media')

MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

PROFILE_UPLOAD_PATH = CKEDITOR_UPLOAD_PATH = 'uploads/'


# Settings related to ratings per section
RATING_SCALE = 10
# For Max digits keep in mind that decimal field is used hence +1 is required
RATING_MAX_DIGITS = 3

# COMMENTS SETTINGS
SECTION_WISE_COMMENTS = True

# Paginate settings
PAGE_NEXT_ITEMS = PAGE_PREVIOUS_ITEMS = 2

AUTH_USER_MODEL = SOCIAL_AUTH_USER_MODEL = 'common.CustomUser'

# Dynamic menus
MAX_MENU_ITEMS = 5
STATIC_MENU_ITEMS = OrderedDict({'Home': '/', 'Contact us': 'contact-us'})

# Socai Auth URLs
SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('blog:blog_list')
SOCIAL_AUTH_LOGIN_ERROR_URL = reverse_lazy('regular_login')
SOCIAL_AUTH_LOGIN_URL = reverse_lazy('regular_login')
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = reverse_lazy('profile')
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = reverse_lazy('profile')
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = reverse_lazy('blog:blog_list')
SOCIAL_AUTH_INACTIVE_USER_URL = reverse_lazy('regular_login')

# Default Meta description and Keywords
#TODO: For now not considering sites
DEFAULT_META_DATA = {
    'description': '',
    'keywords': '',
    'og_type': 'website',
    'site_url': 'https://github.com/kumarvaradarajulu/django-andblog'
}

SITE_NAME = 'DjangoAndBlog'
SITE_FB_ADMINS = ''
SITE_BITLY_VERIFICATION = ''
SITE_URL = 'https://github.com/kumarvaradarajulu/django-andblog'


# SOCIAL LINKS
SOCIAL_LINKS = {
    'twitter': 'http://twitter.com/intent/tweet?status={title}+{url}',
    'facebook': 'http://www.facebook.com/sharer/sharer.php?u={url}&title={title}',
    'googleplus': 'https://plus.google.com/share?url={url}'
}

# BITLY
USE_BITLY = False
BITLY_LOGIN = os.environ.get('BITLY_LOGIN', '')
BITLY_API_KEY = os.environ.get('BITLY_API_KEY', '')

if USE_BITLY:
    INSTALLED_APPS = INSTALLED_APPS + (
        'django_bitly',
    )
