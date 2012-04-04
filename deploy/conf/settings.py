import sys,os.path

DATABASES = {
    'default': {
        'NAME': 'bip',
        'USER': 'bip_user',
        'PASSWORD': 'securityftw', 
        'HOST': 'localhost',
    },

}



SCHEMA_FILE = os.path.abspath('schema/current_schema.sql')

try:
	from localsettings.py import *
except ImportError:
	pass
