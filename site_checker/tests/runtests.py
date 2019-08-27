import sys

import django
from django.conf import settings
from django.core.management import call_command


def runtests():
    if not settings.configured:
        # Choose database for settings
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }

        # Configure test environment
        settings.configure(
            ALLOWED_HOSTS=[],
            DATABASES=DATABASES,
            INSTALLED_APPS=(
                'channels',
                'site_checker',
                'checker_channel',
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.sites',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
            ),
            ROOT_URLCONF='',  # tests override urlconf, but it still needs to be defined
            MIDDLEWARE_CLASSES=(
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),
            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    },
                },
            ],
            # Channels
            ASGI_APPLICATION="egnytex.routing.application",
            CHANNEL_LAYERS = {
                'default': {
                    'BACKEND': 'channels_redis.core.RedisChannelLayer',
                    'CONFIG': {
                        "hosts": [('127.0.0.1', 6379)],
                    },
                },
            },
        )

    if django.VERSION >= (1, 7):
        django.setup()
    failures = call_command(
        'test', 'site_checker', interactive=False, failfast=False, verbosity=2)

    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()

