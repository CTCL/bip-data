'''
Need a centralized place for initiating code. Fiddles with path 
and allows a lo fi way for modules to register commands. 


'''

import sys,os.path,IPython
sys.path.insert(0,os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))

import feedripper.rip

commands = {
	'ripfeed':feedripper.rip,
}

if __name__ == "__main__":
	try:
		print 'via manage.py',sys.argv
		command = sys.argv.pop(1)#it's like the command was never there!
		assert command in commands
	except:
		print "Must invoke one of the following commands:\n%s" % '\n'.join(commands.keys())
		exit()
	data = commands[command].main()#each module should export a main() function that inspects sys.argv itself
	IPython.embed()