#!/usr/bin/env python
'''
Need a centralized place for initiating code. Fiddles with path 
and allows a lo fi way for modules to register commands. 
'''
import sys,os.path,IPython
start_dir = os.curdir
os.chdir('/var/bip')
sys.path.insert(0,os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))
from deploy.conf import settings
import IPython
#Command imports	
import pipeline.feedripper
import deploy.database
from states.base import buildstates
from states.base import bulkbuildstates
import util.modelgeneration
#map command names
import logging
logging.basicConfig(filename='manage.log',level=logging.INFO)

def shell():
	"""Import some things and drop into an IPython shell."""
	from deploy.connections import get_cursor
	cursor = get_cursor()
	IPython.embed()

def bulkbuild():
    deploy.database.drop_fks()
    bulkbuildstates()
#TODO    states.base.resolvefks()
#TODO    deploy.database.buildfks()

#todo: convert this to only import necessary code
commands = {
	'ripfeed':pipeline.feedripper.main,
	'cleandb':deploy.database.clean,
	'dropdb':deploy.database.drop,
	'initdb':deploy.database.init,
	'makedb':deploy.database.make,
	'shell':shell,#todo: allow targets for shell? (i.e. 'bip shell deploy/database.py' would drop you in the scope for the database file?)
	'buildstates':buildstates,
    'bulkbuildstates':bulkbuild,
	'generatemodels':util.modelgeneration.go,
}

if __name__ == "__main__":
	try:
		assert '--help' not in sys.argv#don't judge me -SF
		command = sys.argv.pop(1)#it's like the command was never there!
		assert command in commands
	except:
		commands_listed = '\n\t'.join(["%s: %s" % (k,v.func_doc.strip().split('\n').pop(0) if v.func_doc != None else '') for k,v in commands.iteritems()])
		print "\nMust invoke one of the following commands:\n\n\t%s\n\n" % commands_listed
		exit()
	data = commands[command]()#commands should inspect sys.argv themselves

os.chdir(start_dir)
