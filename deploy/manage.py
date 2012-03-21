#!/usr/bin/env python
'''
Need a centralized place for initiating code. Fiddles with path 
and allows a lo fi way for modules to register commands. 
'''
import sys,os.path,IPython
sys.path.insert(0,os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))
from deploy.conf import settings
import IPython
#Command imports	
import feedripper.rip
import deploy.database

#map command names
commands = {
	'ripfeed':feedripper.rip.main,
	'cleandb':deploy.database.clean,
	'initdb':deploy.database.init,
	'makedb':deploy.database.make,
	'shell':IPython.embed
}


if __name__ == "__main__":
	try:
		assert '--help' not in sys.argv#don't judge me -SF
		command = sys.argv.pop(1)#it's like the command was never there!
		assert command in commands
	except:
		commands_listed = '\n\t'.join(["%s: %s" % (k,v.func_doc.strip().split('\n').pop(0) if v.func_doc != None else '') for k,v in commands.iteritems()])
		print "Must invoke one of the following commands:\n\n\t%s\n\n" % commands_listed
		exit()
	data = commands[command]()#commands should inspect sys.argv themselves

	#IPython.embed(
	#	banner1 = 'Finished running %s. Explore results by inspecting "data"' % command
	# )