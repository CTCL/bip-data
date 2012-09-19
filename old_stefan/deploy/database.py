from deploy.conf import settings
from fabric.api import local
import os.path,sys
import psycopg2
from util.colors import *
schema_fname  = settings.SCHEMA_FILE
schema = open(schema_fname).read()
def get_things_to_drop():
    """Looks at schema and extracts things that need to be explicitly dropped.
    """
    data = schema.split()
    tname = None
    for i in xrange(len(data)):

        x = data[i-1]
        if x.strip() in ['ALTER','CREATE'] and data[i].strip() == 'TABLE':
            #print 'HIT'
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

    name = 'default'
    return settings.DATABASES[name]

def connection(db=get_db_conf()):
    """Dont ever call this on import"""
    print fail('Open %s database connection' % db['NAME'])
    return psycopg2.connect(database=db['NAME'],user=db['USER'],password=db['PASSWORD'])

def init():
    """Add named database user and database"""
    db = get_db_conf()
    sql = get_init_sql(db)
    local('echo "%s" | sudo -u postgres psql' % sql)

def make():
    """Take the current schema and exe it on the named database"""

    sql = open(schema_fname).read()
    print sql
    cursor = connection().cursor()
    cursor.execute('BEGIN;')
    cursor.execute(sql)
    cursor.execute('END;')
    #db = get_db_conf()
    #local('sudo -u postgres psql %s < %s' % (db['NAME'],schema_fname))

def make_no_fks():
    sql = '\n'.join([l.strip() for l in open(schema_fname).readlines() if "FOREIGN KEY" not in l])
    print sql
    cursor = connection().cursor()
    cursor.execute('BEGIN;')
    cursor.execute(sql)
    cursor.execute('END;')

def drop_fks():
    sql = '\n'.join([' '.join(l.strip().split(" ")[:6]).replace('ADD', 'DROP')
        + ';' for l in open(schema_fname).readlines() if "FOREIGN KEY" in l])
    print sql
    cursor = connection().cursor()
    cursor.execute('BEGIN;')
    cursor.execute(sql)
    cursor.execute('END;')

def build_fks():
    sql = '\n'.join([l.strip() for l in open(schema_fname).readlines() if "FOREIGN KEY" in l])
    print sql
    cursor = connection().cursor()
    cursor.execute('BEGIN;')
    cursor.execute(sql)
    cursor.execute('END;')

def drop():
    """"Drop named database"""
    db = get_db_conf()
    sql = get_drop_sql(db)
    local('echo "%s" | sudo -u postgres psql' % sql)
def clean():
    """"Drop named database and initdb and makedb"""
    drop()
    init()
    make()


