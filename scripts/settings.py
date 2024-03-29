import os

env = os.environ.get('ENV')

if env == 'dev':
    print('starting dev environment.....')
    from .settings_development import *
elif env == 'prod':
    print('starting prod environment.....')
    from .settings_production import *
elif env == 'test':
    print('starting test environment.....')
    from .settings_test import *
else:
    print('starting dev environment.....')
    from .settings_development import *