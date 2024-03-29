from .settings_shared import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['test.ubonex.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ubonextw',
        'USER': 'root',
        'PASSWORD': 'qwer1234@',
        'HOST': 'ub-mariadb',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
           'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}