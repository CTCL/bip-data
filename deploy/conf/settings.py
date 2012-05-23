import sys,os.path

DATABASES = {
    'default': {
        'NAME': 'bip3',
        'USER': 'bip_user3',
        'PASSWORD': 'securityftw', 
        'HOST': 'localhost',
    },
    'ohio2': {
        'NAME': 'bip2',
        'USER': 'bip_user2',
        'PASSWORD': 'securityftw', 
        'HOST': 'localhost',
    },
    'ohio': {
        'NAME': 'bip',
        'USER': 'bip_user',
        'PASSWORD': 'securityftw', 
        'HOST': 'localhost',
    },
}



SCHEMA_FILE = os.path.abspath('src/schema/bip_model.sql')
CACHE_FLATTENING = True


try:
	from localsettings.py import *
except ImportError:
	pass
