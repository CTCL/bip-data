import IPython
import os.path
from lxml import etree
import xml.parsers.expat
fname = os.path.abspath('data/vip_feeds/vipFeed-39-2012-03-06.xml')
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


class Bump:
	'''
		Serve up entities off the wire
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
		self.data = None
		self.stack = dict()
		self.mount = self.stack
		self.buffer = ''
		self.i = 0
	def _bump(self):
		print '\nBUMPING\n',self.stack,'\n\n\n'
	def start_element(self, name, attrs):
		print '<%s %s>' % (name, ' '.join('%s="%s"' % (k,v)for k,v in attrs.iteritems())),
		#if name not in self.toss_entities:
		#	self.stack.append(name)
		if name in self.tables:
			print ''
			pref = self.mount
			self.mount[name] = dict(attrs)
			self.mount = self.mount[name]
			self.mount['_parent'] = pref


	def char_data(self, 	data):
		x = data.strip()
		if x != '':
			print x,
			self.buffer += data

	def end_element(self, name):
		data = self.mount
		#print '\n\n\nSTACK\n',self.stack
		assert name not in data
		
		
		if name in self.tables:
			print ''
			self.mount = self.mount.pop('_parent')
		else:
			data[name] = self.buffer
			self.buffer = ''

		print '</%s>' % name

		if '_parent' not in self.mount:
			self._bump()
			self.__init__()
		


def do_expat():
	bump = Bump()
	p = xml.parsers.expat.ParserCreate()
	p.StartElementHandler = bump.start_element
	p.EndElementHandler = bump.end_element
	p.CharacterDataHandler = bump.char_data

	p.ParseFile(open(fname))
	return p

IPython.embed()

keys = [ 
	'vip_object.election ',
	'vip_object.election.absentee_ballot_info',
	'vip_object.election.absentee_request_deadline',
	'vip_object.election.date',
	'vip_object.election.election_day_registration',
	'vip_object.election.election_type',
	'vip_object.election.polling_hours',
	'vip_object.election.registration_deadline',
	'vip_object.election.registration_info',
	'vip_object.election.results_url',
	'vip_object.election.state_id',
	'vip_object.election.statewide',
	'vip_object.election_administration',
	'vip_object.election_administration.elections_url',
	'vip_object.election_administration.eo_id',
	'vip_object.election_administration.hours',
	'vip_object.election_administration.name',
	'vip_object.election_administration.physical_address',
	'vip_object.election_administration.physical_address.city',
	'vip_object.election_administration.physical_address.line1',
	'vip_object.election_administration.physical_address.line2',
	'vip_object.election_administration.physical_address.line3',
	'vip_object.election_administration.physical_address.state',
	'vip_object.election_administration.physical_address.zip',
	'vip_object.election_official',
	'vip_object.election_official.email',
	'vip_object.election_official.fax',
	'vip_object.election_official.name',
	'vip_object.election_official.phone',
	'vip_object.election_official.title',
	'vip_object.electoral_district',
	'vip_object.electoral_district.name',
	'vip_object.electoral_district.type',
	'vip_object.locality',
	'vip_object.locality.election_administration_id',
	'vip_object.locality.name',
	'vip_object.locality.state_id',
	'vip_object.locality.type',
	'vip_object.polling_location',
	'vip_object.polling_location.address',
	'vip_object.polling_location.address.city',
	'vip_object.polling_location.address.line1',
	'vip_object.polling_location.address.line2',
	'vip_object.polling_location.address.location_name',
	'vip_object.polling_location.address.state',
	'vip_object.polling_location.address.zip',
	'vip_object.precinct',
	'vip_object.precinct.locality_id',
	'vip_object.precinct.name',
	'vip_object.precinct_split',
	'vip_object.precinct_split.name',
	'vip_object.precinct_split.polling_location_id',
	'vip_object.precinct_split.precinct_id',
	'vip_object.source',
	'vip_object.source.datetime',
	'vip_object.source.description',
	'vip_object.source.feed_contact_id',
	'vip_object.source.name',
	'vip_object.source.organization_url',
	'vip_object.source.vip_id',
	'vip_object.state',
	'vip_object.state.name',
	'vip_object.street_segment',
	'vip_object.street_segment.end_house_number',
	'vip_object.street_segment.non_house_address',
	'vip_object.street_segment.non_house_address.address_direction',
	'vip_object.street_segment.non_house_address.city',
	'vip_object.street_segment.non_house_address.state',
	'vip_object.street_segment.non_house_address.street_direction',
	'vip_object.street_segment.non_house_address.street_name',
	'vip_object.street_segment.non_house_address.street_suffix',
	'vip_object.street_segment.non_house_address.zip',
	'vip_object.street_segment.odd_even_both',
	'vip_object.street_segment.precinct_id',
	'vip_object.street_segment.precinct_split_id',
	'vip_object.street_segment.start_house_number'
]