import IPython
import os.path
import pprint as pp
import xml.parsers.expat
import timeit
from util.coroutine import coroutine
from util.colors import	blue,green,warn,fail
from pipeline.maps import VipRM
from deploy.database import connection
t = timeit.Timer()

simpleAddressTypes = ["address", "physical_address", "mailing_address", "filed_mailing_address"]
detailAddressTypes = ["non_house_address"]

def sanitize_dict_vals(data):
	for k,v in data.iteritems():
		if type(v) == dict:
			data[k] = sanitize_dict_vals(v)
		else:
			data[k] = None
	data = tuple(sorted([(k,v) for k,v in data.iteritems()]))
	return data

found = set()

@coroutine
def setq():

	cursor = connection().cursor()
	vrm = VipRM(cursor)
	try:
		while True:
			(name,data) = (yield).items().pop()
			print blue(name),warn(data)
			f = vrm.get_mapper(name)
			result = f(data)


				#IPython.embed()

			#	cursor.execute(query)
	except GeneratorExit:
		pass



class Bump:
	'''
		Bump up entities off the wire as dicts from expat handlers
	'''
	related_entities = set(simpleAddressTypes + detailAddressTypes)
	toss_entities = set(['vip_object'])
	#This part is important vv
	primary_entities = set([
		"source",
		"election",
		"locality",
		"precinct",
		"precinct_split",
		"street_segment",
		"polling_location",
		"election_official",
		"electoral_district",
		"election_administration"
	])
	tables = set(list(related_entities) + list(primary_entities))
	
	def __init__(self):
		self.stack = dict()
		self.mount = self.stack
		self.buffer = ''
		self.set = setq()
	def _bump(self):
		self.set.send(self.stack)
		#http://www.dabeaz.com/coroutines/cosax.py
	def start_element(self, name, attrs):
		#print green('<%s %s>' % (name, ' '.join('%s="%s"' % (k,v)for k,v in attrs.iteritems()))),
		if name in self.tables:
			pref = self.mount
			self.mount[name] = dict(attrs)
			self.mount = self.mount[name]
			self.mount['_parent'] = pref
	def char_data(self, 	data):
		self.buffer += data.strip()
	def end_element(self, name):
		data = self.mount
		#print self.buffer,
		#print  green('</%s>' % name)
		#print warn(name),blue(self.stack)
		assert name not in data
		if name in self.tables:
			#print ''
			self.mount = self.mount.pop('_parent')
			if '_parent' not in self.mount:
				self._bump()
				self.__init__()
		else:
			data[name] = self.buffer
			self.buffer = ''



@coroutine
def do_expat():
	try:
		while True:
			fname = (yield)
			print "Ripping %s..." % fname
			bump = Bump()
			p = xml.parsers.expat.ParserCreate()
			p.StartElementHandler = bump.start_element
			p.EndElementHandler = bump.end_element
			p.CharacterDataHandler = bump.char_data
			p.ParseFile(open(fname))
			IPython.embed()
	except GeneratorExit:
		pass

def main():
	"""
		Module must be run from manage.py. 
	"""
	import sys
	fnames = (os.path.abspath(x) for x in sys.argv[1:])
	ripper = do_expat()
	for fname in fnames:
		ripper.send(fname)
	IPython.embed()
