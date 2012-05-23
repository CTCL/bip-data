from util.colors import *
from util.patterns import named_zip
import logging
from collections import defaultdict
#this is a relic from when it was unclear what was required
#make tighter mapping data structures than this one once the mapping needs are clearer
key_map = {
	'election': 'election',
	'election.absentee_ballot_info': 'election.absentee_ballot_info',
	'election.absentee_request_deadline': 'election.absentee_request_deadline',
	'election.date': 'election.date',
	'election.election_day_registration': 'election.election_day_registration',
	'election.election_type': 'election.election_type',
	'election.id': 'election.id',
	'election.polling_hours': 'election.polling_hours',
	'election.registration_deadline': 'election.registration_deadline',
	'election.registration_info': 'election.registration_info',
	'election.results_url': 'election.results_url',
	'election.state_id': 'election.state_id',
	'election.statewide': 'election.statewide',
	'election_administration': 'election_administration',
	'election_administration.elections_url': 'election_administration.elections_url',
	'election_administration.eo_id': 'election_administration.eo_id',
	'election_administration.hours': 'election_administration.hours',
	'election_administration.id': 'election_administration.id',
	'election_administration.name': 'election_administration.name',
	'election_administration.physical_address': 'election_administration.physical_address',
	'election_administration.physical_address.city': None,
	'election_administration.physical_address.line1': None,
	'election_administration.physical_address.line2': None,
	'election_administration.physical_address.line3': None,
	'election_administration.physical_address.state': None,
	'election_administration.physical_address.zip': None,
	'election_official': 'election_official',
	'election_official.email': 'election_official.email',
	'election_official.fax': 'election_official.fax',
	'election_official.id': 'election_official.id',
	'election_official.name': 'election_official.name',
	'election_official.phone': 'election_official.phone',
	'election_official.title': 'election_official.title',
	'electoral_district': 'electoral_district',
	'electoral_district.id': 'electoral_district.id',
	'electoral_district.name': 'electoral_district.name',
	'electoral_district.type': 'electoral_district.type',
	'locality': None,
	'locality.election_administration_id': 'precinct.election_administration_id',
	'locality.name': 'electoral_district.name',
	'locality.state_id': None,
	'locality.type': 'electoral_district.type',
	'polling_location': 'polling_location',
	'polling_location.address': 'polling_location.address',
	'polling_location.address.city': None,
	'polling_location.address.line1': None,
	'polling_location.address.line2': None,
	'polling_location.address.location_name': None,
	'polling_location.address.state': None,
	'polling_location.address.zip': None,
	'polling_location.id': 'polling_location.id',
	'precinct': 'precinct',
	'precinct.id': 'precinct.id',
	'precinct.locality_id': 'precinct.electoral_district_id',
	'precinct.name': 'precinct.name',
	'precinct.polling_location_id': 'precinct.polling_location_id',
	'precinct.electoral_district_id': 'precinct.electoral_district_id',
	'precinct_split': 'precinct',
	'precinct_split.id': 'precinct.id',
	'precinct_split.name': 'precinct.name',
	'precinct_split.polling_location_id': 'precinct.polling_location_id',
	'precinct_split.precinct_id': 'precinct.parent_id',
	'source': 'source',
	'source.datetime': 'source.acquired',
	'source.description': 'source.description',
	'source.feed_contact_id': None,
	'source.id': 'source.id',
	'source.name': 'source.name',
	'source.organization_url': None,
	'source.vip_id': None,
	'state': 'state',
	'state.id': 'state.id',
	'state.name': 'state.name',
	'street_segment': 'street_segment',
	'street_segment.end_house_number': 'street_segment.end_house_number',
	'street_segment.id': 'street_segment.id',
	'street_segment.non_house_address': 'street_segment.non_house_address',
	'street_segment.non_house_address.address_direction': None,
	'street_segment.non_house_address.city': None,
	'street_segment.non_house_address.state': None,
	'street_segment.non_house_address.street_direction': None,
	'street_segment.non_house_address.street_name': None,
	'street_segment.non_house_address.street_suffix': None,
	'street_segment.non_house_address.zip': None,
	'street_segment.odd_even_both': 'street_segment.odd_even_both',
	'street_segment.precinct_id': 'street_segment.precinct_id',
	'street_segment.precinct_split_id': 'street_segment.precinct_id**',
	'street_segment.start_house_number': 'street_segment.start_house_number'
}


fk_map = {
	#'address': 'geo_address',
	'election_administration_id': 'election_administration',
	'electoral_district_id': 'electoral_district',
	'eo_id': 'election_official',
	'feed_contact_id': 'election_official',#is this right?
	'locality_id': 'electoral_district',
	#'non_house_address': 'geo_address',
	#'physical_address': 'geo_address',
	'polling_location_id': 'polling_location',
	'precinct_id': 'precinct',
	'precinct_split_id':'precinct',
	'parent_id': 'precinct',
	'precinct_split_id': 'precinct',
	'state_id': 'state',
	#'vip_id': 'source'
}
#id -> source_pk
#identify fk's 
#map fk identifiers to table names
#queue refs needing actual pk's
#2nd pass


def sqlescape(x):
	if type(x) in (unicode, str):
		x = x.replace('\'','\'\'')
	else:
		x = str(x)
	return '\'' + x + '\'' if x != '' else 'NULL'


class VipRM:
	"""
		Relational Mapping for VIP XML: Used to insert data.
	"""
	pk = {}#index of all source pk's to actual pk's
	fk_q = []#holds orphaned foriegn key information
	errors = []#not that important, handy when debugging
	valid_fields = dict()
	def __init__(self,cursor):
		self.cursor = cursor
	def _insert(self,data,name,table_override=None):
		store_pk = 'id' in data##$
		sql = self._dict_to_sql(data,name,table_override)
		logging.info(sql)
		self.cursor.execute('BEGIN;')
		self.cursor.execute(sql)
		pk = self.cursor.fetchone()[0]
		data['id'] = pk
		self.cursor.execute('END;')
		if store_pk:##$
			local_key = (name,data['source_pk'])
			logging.info((local_key,pk,self.pk[local_key] if local_key in self.pk else None))
			assert local_key not in self.pk
			self.pk[local_key] = pk#need to do fk's in a 2nd pass
		return pk
	def _dict_to_sql(self,data,name,table_override):
		if 'id' in data:
			data['source_pk'] = data.pop('id')
		fields = data.keys()
		fks = [x for x in fields if x in fk_map]
		logging.info((name,fields))
		logging.info((fks,data))
		for fk in fks:
			data = self._fix_fk(data,fk,fk_map[fk],name)
		if table_override != None:
			name = table_override
		values = [sqlescape(data[k]) if data[k] != None else 'NULL' for k in data.iterkeys()]
		return "insert into %s (%s) VALUES (%s) RETURNING id;" % (name,', '.join(fields),', '.join(values))

	def _fix_fk(self,data,fk_name,dest_model_name,home_model_name):
		fk_val = data[fk_name]
		local_key = (dest_model_name,fk_val)
		logging.info(green(local_key))
		if local_key in self.pk:
			data[fk_name] = self.pk[local_key]
		else:#the referenced object has not been seen yet
			fk_val = data[fk_name]
			data[fk_name] = None
			self.fk_q.append((data,fk_name,fk_val,dest_model_name,home_model_name))
		return data

			 
	def _insert_address(self,address_data):
		zips = named_zip.match(address_data['zip'])
		if zips != None:
			zips = dict(((k,v) for k,v in zips.groupdict().iteritems() if v != None and v in ['zip','zip4']))
			address_data.pop('zip')
			address_data.update(zips)
		return self._insert(address_data,'geo_address')
		
	def _insert_addresses(self,data):
		address_fields = ((k.split('.'),data.pop(k)) for k in data.keys() if 'address.' in k)
		address_fields = ((k[0],k[1],v) for k,v in address_fields)
		addresses = defaultdict(lambda: dict())
		for k1,k2,v in address_fields:
			addresses[k1][k2] = v
		logging.info(blue(addresses))

		for k,address_data in addresses.iteritems():
			data[k] = self._insert_address(address_data)
		return data

	def _push_polling_location_to_db(self,data,name='polling_location'):
		data = self._insert_addresses(data)
		return self._insert(data,name)
	def _push_precinct_split_to_db(self,data,name='precinct_split'):
		#data['parent_id'] = data.pop('precinct_id')
		return self._insert(data,name,table_override='precinct')

	def _push_locality_to_db(self,data,name='electoral_district'):
		data.pop('election_administration_id')
		data.pop('early_vote_site_id')
		return self._insert(data,name)

	def _push_state_to_db(self,data,name='state'):
		data.pop('election_administration_id')
		data.pop('early_vote_site_id')
		return self._insert(data,name)

	def _push_electoral_district_to_db(self,data,name='electoral_district'):
		return self._insert(data,name)

	def _push_source_to_db(self,data,name='source'):
		#data['acquired'] = data.pop('datetime')
		data['id'] = data.pop('vip_id')
		data.pop('feed_contact_id')
		data.pop('tou_url')
		return self._insert(data,name)

	def _push_street_segment_to_db(self,data,name='street_segment'):
		data = self._insert_addresses(data)
		return self._insert(data,name)

	def _push_precinct_to_db(self,data,name='precinct'):
		print data
		#data['electoral_district_id'] = data.pop('locality_id')#natural id's less likely to be unique across entities!
		return self._insert(data,name)

	def _push_election_official_to_db(self,data,name='election_official'):
		return self._insert(data,name)

	def _push_election_to_db(self,data,name='election'):
		return self._insert(data,name)

	def _push_election_administration_to_db(self,data,name='election_administration'):
		data = self._insert_addresses(data)

		return self._insert(data,name)

	def get_mapper(self,name):
		return getattr(self,'_push_%s_to_db' % name)

	def flush(self):
		
		for data,fk_name,fk_val,dest_model_name,home_model_name in self.fk_q:
			try:
				logging.info(warn(data))
				for k,v in data.iteritems():
					if v == None:
						local_key_via_fk = (dest_model_name,fk_val)
						logging.info(local_key_via_fk)
						if local_key_via_fk not in self.pk:
							logging.info(fail('Does not compute. Inspect \'self\'.'))
							self.errors.append(('Key Not Found',data,fk_name,fk_val,dest_model_name,home_model_name))
						#ISSUE ALTER TABLE
						fk_val_global = self.pk[local_key_via_fk]
						q = '''UPDATE %s SET %s = %s WHERE id = %s;''' % (
							home_model_name,
							fk_name,
							fk_val_global,
							data['id']
						)
						logging.info(green(q))
						self.cursor.execute(q)
						assert local_key_via_fk in self.pk
			except:
				self.errors.append(('Exception',data,fk_name,fk_val,dest_model_name,home_model_name))
