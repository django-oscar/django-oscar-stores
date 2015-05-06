import os

from django.conf import settings
from oscar.defaults import OSCAR_SETTINGS
from oscar import OSCAR_MAIN_TEMPLATE_DIR, get_core_apps


def pytest_configure():
    location = lambda x: os.path.join(
        os.path.dirname(os.path.realpath(__file__)), x)

    test_settings = OSCAR_SETTINGS.copy()
    test_settings.update(dict(
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'oscar_stores',
                'HOST': '127.0.0.1',
            }
        },
        SITE_ID=1,
        MEDIA_ROOT=location('public/media'),
        MEDIA_URL='/media/',
        STATIC_URL='/static/',
        STATICFILES_DIRS=(location('static/'),),
        STATIC_ROOT=location('public'),
        STATICFILES_FINDERS=(
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ),
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATE_CONTEXT_PROCESSORS=(
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.request",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "django.contrib.messages.context_processors.messages",
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'oscar.apps.basket.middleware.BasketMiddleware',
        ),
        ROOT_URLCONF='sandbox.sandbox.urls',
        TEMPLATE_DIRS=(
            location('templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ),
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
            'django.contrib.gis',
            'django.contrib.flatpages',
            'compressor',
            'widget_tweaks',
        ] + get_core_apps() + [
            'stores',
        ],
        AUTHENTICATION_BACKENDS=(
            'oscar.apps.customer.auth_backends.Emailbackend',
            'django.contrib.auth.backends.ModelBackend',
        ),
        LOGIN_REDIRECT_URL='/accounts/',
        APPEND_SLASH=True,
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
            },
        },
        GEOIP_PATH='sandbox/geoip',
        COMPRESS_ENABLED=False,
        TEST_RUNNER='django.test.runner.DiscoverRunner',
    ))
    settings.configure(**test_settings)
