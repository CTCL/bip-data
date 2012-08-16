from ersatzpg import ersatz
from data.voterfiles.oh import state_conf
from schema import process_schema, table_tools
import time, sys, imp, os

tables, enums, fks, seqs = process_schema.rip_schema('schema/bip_model_cleaned.sql')
table_tools.define_long_tables(tables, fks)
if '-b' in sys.argv:
    state = sys.argv[sys.argv.index('-b') + 1].lower()
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    from state_conf import *
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.delete_long_tables(tables, connection)
    table_tools.create_long_tables(tables, connection)
    connection.cursor().execute('DROP TABLE IF EXISTS voter_file CASCADE;')
    connection.cursor().execute(open(state_conf.VOTER_FILE_SCHEMA,'r').read())
    ersatz.new_process_copies(state_conf, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-n' in sys.argv:
    state = sys.argv[sys.argv.index('-n') + 1].lower()
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    from state_conf import *
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.delete_tables(tables, connection)
    table_tools.create_tables(tables, connection)
    connection.cursor().execute('DROP TABLE IF EXISTS voter_file CASCADE;')
    connection.cursor().execute(open(state_conf.VOTER_FILE_SCHEMA,'r').read())
    ersatz.new_process_copies(state_conf, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-p' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.pk_tables(tables, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-r' in sys.argv:
    t = time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.delete_tables(tables, connection)
    table_tools.rekey_tables(tables, fks, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
