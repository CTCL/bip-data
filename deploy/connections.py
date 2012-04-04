from deploy.conf import settings
import psycopg2


def get_db_conn(name='default'):
	db = settings.DATABASES[name]
	return psycopg2.connect(database=db['NAME'], user=db['USER'], password=db['PASSWORD'])

def get_cursor(name='default'):
	return get_db_conn(name=name).cursor()