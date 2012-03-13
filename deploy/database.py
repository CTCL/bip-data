from deploy.conf import settings
from fabric.api import local
import os.path,sys


schema_fname  = os.path.abspath('src/schema/bip_model_0.4.sql')
schema = open(schema_fname).read()
def get_things_to_drop():
	data = schema.split()
	tname = None
	for i in xrange(len(data)):

		x = data[i-1]
		if x.strip() in ['ALTER','CREATE'] and data[i].strip() == 'TABLE':
			print 'HIT'
			tname = data[i+1]

		if x in ['CONSTRAINT']:
			#print ' '.join(data[i-8:i+4])
			assert tname != None

			yield 'ALTER TABLE %s DROP %s "%s" CASCADE;' % (tname,data[i-1],data[i].strip('"'))

		elif x in ['TYPE']:
			assert tname == None
			yield 'DROP %s "%s" CASCADE;' % (data[i-1],data[i].strip('"'))


def get_init_sql(db):
	return '''
	create user %s with password '%s' CREATEDB;                                                          
	CREATE DATABASE %s
	       WITH OWNER = %s                                                                     
	       ENCODING = 'UTF8'                                                  
	       LC_COLLATE = 'en_US.UTF-8'
	       LC_CTYPE = 'en_US.UTF-8'
	       CONNECTION LIMIT = -1;
	''' % (db['USER'],db['PASSWORD'],db['NAME'],db['USER'])

def get_drop_sql(db):
	return '''
	drop database %s;
	drop user %s;
	''' % (db['NAME'],db['USER']) + '\n'.join([x for x in get_things_to_drop()])

def get_db_conf():
	if len(sys.argv) > 1:
		name = sys.argv[1]
	else:
		name = 'default'
	return settings.DATABASES[name]

def init():
	"""Add named database user and database"""
	db = get_db_conf()
	sql = get_init_sql(db)
	local('echo "%s" | sudo -u postgres psql' % sql)

def make():
	"""Take the current schema and exe it on the named database"""
	db = get_db_conf()
	local('sudo -u postgres psql %s < %s' % (db['NAME'],schema_fname))
def clean():
	""""Drop named database and initdb and makedb"""
	db = get_db_conf()
	sql = get_drop_sql(db)
	local('echo "%s" | sudo -u postgres psql' % sql)
	init()
	

