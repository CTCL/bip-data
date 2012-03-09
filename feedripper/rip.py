import IPython
import os.path
from lxml import etree
import xml.parsers.expat
import timeit
from util.coroutine import coroutine
t = timeit.Timer()

simpleAddressTypes = ["address", "physical_address", "mailing_address", "filed_mailing_address"]
detailAddressTypes = ["non_house_address"]
def do_lxml():
	vip_id = 32
	xmlparser = etree.XMLParser()
	data = etree.parse(open(fname), xmlparser)
	root = data.getroot()
	elements = root.getchildren()
	def tag_ripper(elem,prefix):
		tag = "%s.%s" % (prefix,elem.tag)
		yield tag
		for c in elem.getchildren():
			for t in tag_ripper(c,tag):
				yield t.strip('.')
	#keys = set(tag_ripper(root,''))

all_data = list()

class Bump:
	'''
		Bump up entities off the wire as dicts from expat handlers
	'''
	related_entities = set(simpleAddressTypes + detailAddressTypes)
	toss_entities = set(['vip_object'])
	primary_entities = set([
		"source",
		"election",
		"locality",
		"precinct",
		"street_segment",
		"polling_location"
	])
	tables = set(list(related_entities) + list(primary_entities))
	def __init__(self):
		self.stack = dict()
		self.mount = self.stack
		self.buffer = ''
	def _bump(self):
		#set.send(self.stack)
		all_data.append(self.stack)
		#print '\nBUMPING\n',self.stack
		#http://www.dabeaz.com/coroutines/cosax.py
	def start_element(self, name, attrs):
		#print '<%s %s>' % (name, ' '.join('%s="%s"' % (k,v)for k,v in attrs.iteritems())),
		if name in self.tables:
			#print ''
			pref = self.mount
			self.mount[name] = dict(attrs)
			self.mount = self.mount[name]
			self.mount['_parent'] = pref
	def char_data(self, 	data):
		self.buffer += data.strip()
	def end_element(self, name):
		data = self.mount
		assert name not in data
		if name in self.tables:
			#print ''
			self.mount = self.mount.pop('_parent')
		else:
			data[name] = self.buffer
			self.buffer = ''
		#print '</%s>' % name
		if '_parent' not in self.mount:
			self._bump()
			self.__init__()

@coroutine
def do_expat():
	fname = (yield)
	print "Ripping %s..." % fname
	bump = Bump()
	p = xml.parsers.expat.ParserCreate()
	p.StartElementHandler = bump.start_element
	p.EndElementHandler = bump.end_element
	p.CharacterDataHandler = bump.char_data
	p.ParseFile(open(fname))

def main():
	"""
		Module must be run from manage.py. 
	"""
	import sys
	fnames = (os.path.abspath(x) for x in sys.argv[1:])
	ripper = do_expat()
	for fname in fnames:
		ripper.send(fname)
