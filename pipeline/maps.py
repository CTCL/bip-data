from util.colors import *
from util.patterns import named_zip
import logging
from collections import defaultdict



fk_map = {

	'election_administration_id': 'election_administration',
	'electoral_district_id': 'electoral_district',
	'eo_id': 'election_official',
	'feed_contact_id': 'election_official',#is this right?
	'locality_id': 'electoral_district',
	'polling_location_id': 'polling_location',
	'precinct_id': 'precinct',
	'precinct_split_id':'precinct',
	'parent_id': 'precinct',
	'precinct_split_id': 'precinct',
	'state_id': 'state',

}



def sqlescape(x):
	'''
	Escapes specific values withing the context of an insert statement
	room to get much fancier here'
	'''

	if type(x) in (unicode, str):
		x = x.replace('\'','\'\'')
	else:
		x = str(x)
	return '\'' + x + '\'' if x != '' else 'NULL'


class VipInserter:
	"""
		Relational Mapping for VIP XML: Used to insert data.
	"""
	pk = {}#index of all source pk's to actual pk's
	fk_q = []#holds orphaned foriegn key information
	errors = []#not that important, handy when debugging
	valid_fields = dict()
	insert_queue = list()
	transaction_open = False
	def __init__(self,cursor):
		self.cursor = cursor
	def _flush_inserts(self):
		if not self.transaction_open:
			self.cursor.execute('BEGIN;')
			self.transaction_open = True
		for sql in self.insert_queue:
			self.cursor.execute(sql)
		self.cursor.execute('END;')
		self.transaction_open = False
		self.insert_queue = list()

	def _insert(self,data,name,table_override=None,store_pk=None):
		if store_pk == None:
			store_pk = 'id' in data##$
		sql = self._dict_to_sql(data,name,table_override)
		logging.info(sql)


		logging.info(('WAT?',(store_pk,len(self.insert_queue))))
		if not store_pk and len(self.insert_queue) < 100:
			#no need to spend a transaction on this
			self.insert_queue.append(sql)
			logging.info(('queueing',sql))
			return
		elif not store_pk and len(self.insert_queue) >= 100:
			logging.info('######FLUSHING INSERTS####')
			self.insert_queue.append(sql)
			self._flush_inserts()
			return
		elif store_pk:##$
			if not self.transaction_open:
				self.cursor.execute('BEGIN;')
				self.transaction_open = True
			self.cursor.execute(sql)
			pk = self.cursor.fetchone()[0]
			self.cursor.execute('END;')
			self.transaction_open = False
			data['id'] = pk
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
		if table_override != None:#this can probably be done better before here
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
		return self._insert(data,name,store_pk=False)

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
		self._flush_inserts()
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
