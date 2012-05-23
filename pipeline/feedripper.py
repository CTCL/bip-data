import IPython
import sys,os,os.path,shutil
import pprint as pp
import xml.parsers.expat
import timeit
from util.coroutine import coroutine
from util.colors import	blue,green,warn,fail
from pipeline.maps import VipRM
from deploy.database import connection
import logging,csv
from vip.vave.feed_destructor.feed_to_flatfiles import FeedToFlatFiles
from deploy.conf.fieldnames import vip_to_bip_names
from deploy.conf import settings

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

	print fail('COROUTINE CALLED')
	

	try:
		while True:
			(name,data) = (yield).items().pop()


			logging.info((blue(name),warn(data)))
			f = vrm.get_mapper(name)
			result = f(data)


			

			#	cursor.execute(query)
	except GeneratorExit:
		print fail('Generator Exit')
		vrm.flush()




class Bump:
	'''
		Bump up entities off the wire as dicts from expat handlers
	'''
	related_entities = set(simpleAddressTypes + detailAddressTypes)
	toss_entities = set(['vip_object'])
	#This part is important vv
	primary_entities = set([
		"source",
		"state",
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
	set = None
	def __init__(self):
		self.stack = dict()
		self.mount = self.stack
		self.buffer = ''
		if self.set == None: self.set = setq()
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
			#IPython.embed()
	except GeneratorExit:
		pass

def fieldname(ename,fieldname):
	new_fieldname = vip_to_bip_names['%s.%s' % (ename,fieldname)]
	return new_fieldname if new_fieldname != None else fieldname

def flip_file(path):
	temp_path = path + '.headertransformed'
	fdir,fname = os.path.split(path)
	entity_name = fname.replace('.txt',''	)
	in_file = open(path)
	out_file = open(temp_path,'w')
	old_header= in_file.readline().strip().split(',')

	new_header = [fieldname(entity_name,x) for x in old_header]
	out_file.write(','.join(new_header) + '\n')
	for line in in_file:
		out_file.write(line)
	in_file.close()
	out_file.close()
	os.remove(path)
	shutil.move(temp_path,path)



@coroutine
def do_viacsv():
	try:
		while True:
			rel_path = (yield)
			print "Ripping %s..." % rel_path
			#file operations
			abs_path = os.path.abspath(rel_path)
			local_root,fname = os.path.split(abs_path)
			csv_root = os.path.join(local_root,'%s.flattened' % fname)
			csv_file_paths = [os.path.join(csv_root,fname) for fname in os.listdir(csv_root)]
			if not os.path.isdir(csv_root) or not settings.CACHE_FLATTENING:
				if os.path.isdir(csv_root):
					shutil.rmtree(csv_root)
				os.mkdir(csv_root)
				ftff = FeedToFlatFiles(csv_root)
				ftff.process_feed(abs_path)
				
				for fpath in csv_file_paths:
					flip_file(fpath)
			else:
				print '%s: Skipping flattening' % "Files exist" if os.path.isdir(csv_root) else "Files cached"
			#iterating through all data
			cursor = connection().cursor()
			vrm = VipRM(cursor)
			for fpath in csv_file_paths:
				fdir,fname = os.path.split(fpath)
				entity_name = fname.replace('.txt',''	)
				for data in csv.DictReader(open(fpath)):
					logging.info((blue(entity_name),warn(data)))
					f = vrm.get_mapper(entity_name)
					result = f(data)
			#for entity in files: bump to db

	except GeneratorExit:
		pass


def main():
	"""
		Module must be run from manage.py. 
	"""
	
	fnames = (os.path.abspath(x) for x in sys.argv[1:])
	ripper = do_expat()
	for fname in fnames:
		ripper.send(fname)
	


