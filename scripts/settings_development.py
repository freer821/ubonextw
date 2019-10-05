from .settings_shared import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ubonextw',
        'USER': 'root',
        'PASSWORD': 'qwer1234@',
        'HOST': '192.168.178.108',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
           'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}