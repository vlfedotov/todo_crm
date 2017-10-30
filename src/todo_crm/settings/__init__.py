import os


env = os.getenv('TODOCRM_ENV', 'develop')

if env == 'develop':
    from .base import *
elif env == 'testing':
    from .test import *
else:
    raise ValueError('unknown environment: {}'.format(env))

