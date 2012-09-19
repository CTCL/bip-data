
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def blue(text):
	return "%s%s%s" % (OKBLUE,text,ENDC)
def green(text):
	return "%s%s%s" % (OKGREEN,text,ENDC)
def warn(text):
	return "%s%s%s" % (WARNING,text,ENDC)
def fail(text):
	return "%s%s%s" % (FAIL,text,ENDC)