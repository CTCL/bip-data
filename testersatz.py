from ersatzpg import ersatz
from schema import process_schema, table_tools, create_partitions, create_precinct_to_ed
from state_abbr import states
import time, sys, imp, os

state = sys.argv[-1].lower()
state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
state_conf = imp.load_source('state_conf', state_conf)
from state_conf import *
tables, enums, fks, seqs = process_schema.rip_schema('schema/bip_model_cleaned.sql')
table_tools.define_long_tables(tables, fks)


if '-t' in sys.argv:
    table_subset = eval(sys.argv[sys.argv.index('-t') + 1])
    table_subdict = dict([(t, tables[t]) for t in tables.keys() if t in table_subset])
else:
    table_subdict = tables

if '-clean_keyed' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.delete_tables(tables, connection)
    table_tools.create_tables(tables, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-clean' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.delete_tables(tables, connection)
    table_tools.create_tables(tables, connection)
    table_tools.delete_import_tables(ACTUAL_TABLES, UNIONS, connection)
    table_tools.create_import_tables(ACTUAL_TABLES, tables, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-d' in sys.argv:
    state = sys.argv[-1].lower()
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    from state_conf import *
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    #connection.cursor().execute('DROP TABLE IF EXISTS voter_file CASCADE;')
    #connection.cursor().execute(open(state_conf.VOTER_FILE_SCHEMA,'r').read())
    finished_schema_tables = []
    for table in ACTUAL_TABLES:
        if table['schema_table'] not in finished_schema_tables:
            finished_schema_tables.append(table['schema_table'])
            create_partitions.create_discrete_partitions([table['schema_table']], {'source':table['import_table']['sources'],'election_key':table['import_table']['elections']}, connection.cursor())
            connection.commit()
                #create_partitions.create_discrete_partitions([tname for tname in ['precinct','electoral_district','electoral_district__precinct','locality'] if tname in table_subset], {'source':[s+'VF' for s in states],'election_key':['2012']}, connection.cursor())
                #create_partitions.create_discrete_partitions([tname for tname in ['candidate_long','contest_long','candidate_in_contest_long'] if tname in table_subset], {'source':[s+'Candidates' for s in states],'election_key':['2012']}, connection.cursor())
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-b' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    #state_conf.ERSATZPG_CONFIG['tables'] = dict([(tname,state_conf.ERSATZPG_CONFIG['tables'][tname]) for tname in state_conf.ERSATZPG_CONFIG['tables'] if tname in table_subset])
    #state_conf.ERSATZPG_CONFIG['parallel_load'] = tuple(p for p in state_conf.ERSATZPG_CONFIG['parallel_load'] if all(tab in table_subset for tab in p['tables']))
    for group_name, group in state_conf.GROUPS.iteritems():
        state_conf.ERSATZPG_CONFIG['tables'].update({group_name:table_tools.create_import_group(group_name, group, tables, connection)})
    ersatz.new_process_copies(state_conf, connection)
    for group_name, group in state_conf.GROUPS.iteritems():
        table_tools.split_group_tables(group_name, group, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-grouptest' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    for group_name, group in state_conf.GROUPS.iteritems():
        table_tools.split_group_tables(group_name, group, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-distinct' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.distinct_imports(ACTUAL_TABLES, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-unions' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.create_union_tables(ACTUAL_TABLES, tables, UNIONS, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-rekey' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.rekey_imports(ACTUAL_TABLES, UNIONS, tables, connection, ['source','election_key'])
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)

if '-j' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    for s in states:
        create_precinct_to_ed.create_joined(s, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-count' in sys.argv:
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    for s in states:
        create_precinct_to_ed.make_counts(s, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-p' in sys.argv:
    state = sys.argv[-1].lower()
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    t =time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    table_tools.pk_tables(table_subdict, connection)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
if '-r' in sys.argv:
    state = sys.argv[-1].lower()
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    t = time.time()
    connection = ersatz.db_connect(state_conf.ERSATZPG_CONFIG)
    create_partitions.create_discrete_partitions([tname for tname in ['candidate', 'contest','candidate_in_contest'] if tname in table_subset], {'source':[s+'Candidates' for s in states],'election_key':['2012']}, connection.cursor())
    table_tools.rekey_insert_tables(dict([(tname,table_subdict[tname]) for tname in table_subdict if tname in ['candidate','candidate_in_contest','contest']]), fks, connection, source=state_conf.STATE + 'Candidates', election_key=2012)
    connection.commit()
    connection.close()
    t = time.time() - t
    print "Elapsed: %s" % (t,)
