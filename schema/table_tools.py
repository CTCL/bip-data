import os
def define_long_tables(table_dict, fks):
    for fk in fks:
        for fro, to in fk.reference_fields.iteritems():
            table_dict[fk.table].fields[fro].long_from = True
            table_dict[fk.reference_table].fields[to].long_to = True

def rekey_tables(table_dict, fks, dbconn):
    for k,v in table_dict.iteritems():
        if v.has_long():
            tfks = [fk for fk in fks if fk.table == k]
            sql, data = v.rekey(tfks)
            print sql % data
            dbconn.cursor().execute(sql % data)

def rekey_insert_tables(table_dict, fks, dbconn, **split_keys):
    for k,v in table_dict.iteritems():
        if v.has_long():
            tfks = [fk for fk in fks if fk.table == k]
            sql, data = v.rekey_insert(tfks, **split_keys)
            print sql
            dbconn.cursor().execute(sql)

def delete_import_tables(actual_tables, unions, connection):
    for table in actual_tables:
        sql = 'DROP TABLE IF EXISTS {name} CASCADE;'.format(name=table['import_table']['table'])
        print sql
        connection.cursor().execute(sql)
        sql = 'DROP TABLE IF EXISTS {name}_distinct CASCADE;'.format(name=table['import_table']['table'])
        print sql
        connection.cursor().execute(sql)
    for union in unions:
        sql = 'DROP TABLE IF EXISTS {name} CASCADE;'.format(name=union['name'])
        print sql
        connection.cursor().execute(sql)

def create_import_tables(actual_tables, table_dict, connection):
    created_tables = set()
    for table in actual_tables:
        if table['import_table']['table'] in created_tables:
            continue
        created_tables.add(table['import_table']['table'])
        sql = table_dict[table['schema_table']].sql_import(table)
        print sql
        connection.cursor().execute(sql)

def create_import_group(group_name, group, table_dict, connection):
    sql = 'CREATE TABLE {name} ({fields});'.format(name=group_name, fields=','.join(table_dict[table['schema_table']].sql_fields(table, table['import_table']['table']) for table in group['tables']))
    print sql
    connection.cursor().execute(sql)
    import_table = dict(group['default'])
    import_table.update({'table':group_name, 'udcs':{}, 'columns':{}})
    for table in group['tables']:
        prefix = table['import_table']['table']
        import_table['udcs'].update(dict([('{prefix}_{key}'.format(prefix=prefix,key=k),v) for k,v in table['import_table']['udcs'].iteritems()]))
        import_table['columns'].update(dict([('{prefix}_{key}'.format(prefix=prefix,key=k),v) for k,v in table['import_table']['columns'].iteritems()]))
    return import_table

def split_group_tables(group_name, group, connection):
    for table in group['tables']:
        sql = 'INSERT INTO {name}({fields}) SELECT {prefix_fields} from {group_table};'.format(name=table['import_table']['table'], group_table=group_name, fields=','.join(k for k in table['import_table']['udcs'].keys() + table['import_table']['columns'].keys()), prefix_fields=','.join('{prefix}_{key}'.format(prefix=table['import_table']['table'], key=k) for k in table['import_table']['udcs'].keys() + table['import_table']['columns'].keys()), distinct_clause = ('DISTINCT ON ({fields})'.format(fields=','.join('{prefix}_{dist}'.format(prefix=table['import_table']['table'],dist = dist) for dist in table['distinct_on'])) if table.has_key('distinct_on') else ''))
        print sql
        connection.cursor().execute(sql)

def create_union_tables(actual_tables, table_dict, unions, connection):
    actual_table_dict = dict([(a['import_table']['table'],a) for a in actual_tables])
    for union in unions:
        first_component = union['components'][0]
        table = actual_table_dict[first_component]
        sql = table_dict[table['schema_table']].sql_import(table, union['name'])
        print sql
        connection.cursor().execute(sql)
        for c in union['components']:
            table = actual_table_dict[c]
            sql = 'ALTER TABLE {name} INHERIT {parent};'.format(name=c + ('_distinct' if table.has_key('distinct_on') else ''),parent=union['name'])
            print sql
            connection.cursor().execute(sql)

def distinct_imports(actual_tables, connection):
    for table in actual_tables:
        if table.has_key('distinct_on'):
            sql = 'CREATE TABLE {import_table}_distinct as SELECT DISTINCT ON ({distinct_fields}) * from {import_table};'.format(distinct_fields=','.join(table['distinct_on']), import_table=table['import_table']['table'])
            print sql
            connection.cursor().execute(sql)
            connection.cursor().execute('DROP TABLE {import_table}'.format(import_table=table['import_table']['table']))
            table['rekey_table_name'] = table['import_table']['table']+'_distinct'

def rekey_imports(actual_tables, unions, table_dict, connection, split_names, special_tables):
    actual_table_dict = dict([(a['import_table']['table'],a) for a in actual_tables])
    rekey_table_dict = dict([(a['import_table']['table'],a['import_table']['table']+('_distinct' if a.has_key('distinct_on') else '')) for a in actual_tables] +[(u['name'],u['name']) for u in unions] + [(s,s) for s in special_tables])
    cleared_tables = set()
    for table in actual_tables:
        if table.has_key('distinct_on'):
            table['rekey_table_name'] = table['import_table']['table']+'_distinct'
    for table in actual_tables:
        if len(table['long_fields']) > 0:
            split_keys = dict([(tkey,tval) for tkey, tval in table['import_table']['udcs'].iteritems() if tkey in split_names])
            if table['schema_table'] not in cleared_tables:
                clear_sql = 'DELETE from {name}'.format(name=table['schema_table']) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_names).format(**split_keys) + ';'
                print clear_sql
                connection.cursor().execute(clear_sql)
                cleared_tables.add(table['schema_table'])
            sql = table_dict[table['schema_table']].rekey_imports(table, rekey_table_dict, **split_keys)
            print sql
            connection.cursor().execute(sql)
        else:
            split_keys = dict([(tkey,tval) for tkey, tval in table['import_table']['udcs'].iteritems() if tkey in split_names])
            sql = 'CREATE TABLE {name}'.format(name=table['schema_table']) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_names).format(**split_keys) + ';'
            print sql
            connection.cursor().execute(sql)

def export_referenda_tables(election, out_dir, connection):
    sql = "COPY {table}_referenda_{election} TO '{out_dir}{ossep}{table}.csv' CSV HEADER;"
    connection.cursor().execute(sql.format(table='contest', out_dir=out_dir, election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='referendum', out_dir=out_dir, election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='ballot_response', out_dir=out_dir, election=election, ossep = os.sep))

def export_presidential_tables(election, out_dir, connection):
    state = 'presidential'
    sql = "COPY {table}_{source}_{election} TO '{out_dir}{ossep}{table}.csv' CSV HEADER;"
    connection.cursor().execute(sql.format(table='candidate', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='candidate_in_contest', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='contest', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))

def export_candidate_tables(state, election, out_dir, connection):
    sql = "COPY {table}_{source}_{election} TO '{out_dir}{ossep}{table}.csv' CSV HEADER;"
    connection.cursor().execute(sql.format(table='candidate', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='candidate_in_contest', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='contest', out_dir=out_dir, source=state+'candidates', election=election, ossep = os.sep))
    connection.cursor().execute(sql.format(table='electoral_district', out_dir=out_dir, source=state+'VF', election=election, ossep = os.sep))

def create_long_tables(table_dict, connection):
    for t in table_dict.values():
        sql, data = t.sql_data(True)
        print sql % data
        connection.cursor().execute(sql % data)

def delete_long_tables(table_dict, connection):
    for t in table_dict:
        connection.cursor().execute('DROP TABLE IF EXISTS %s_long CASCADE;'% (t,))

def create_tables(table_dict, connection):
    for t in table_dict.values():
        sql, data = t.sql_data(False, True)
        print sql % data
        connection.cursor().execute(sql % data)

def delete_tables(table_dict, connection):
    for t in table_dict:
        connection.cursor().execute('DROP TABLE IF EXISTS %s CASCADE;'%(t,))

def delete_pksq(connection):
    connection.cursor().execute('DROP SEQUENCE IF EXISTS PKSQ CASCADE;')

def create_pksq(connection):
    connection.cursor().execute('CREATE SEQUENCE PKSQ START 1;')

def delete_enums(connection):
    sql = """
    DROP TYPE IF EXISTS contestenum CASCADE;
    DROP TYPE IF EXISTS cfenum CASCADE;
    DROP TYPE IF EXISTS electionenum CASCADE;
    DROP TYPE IF EXISTS oddevenenum CASCADE;
    DROP TYPE IF EXISTS usstate CASCADE;
    """
    connection.cursor().execute(sql)

def create_enums(connection):
    sql = """
    CREATE TYPE contestenum AS ENUM ('candidate','referendum','custom');
    CREATE TYPE cfenum AS ENUM ('candidate','referendum ');
    CREATE TYPE electionenum AS ENUM ('primary','general','state','Primary','General','State');
    CREATE TYPE oddevenenum AS ENUM ('odd','even','both','BOTH','EVEN','ODD');
    CREATE TYPE usstate AS ENUM ('AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MH', 'MA', 'MI', 'FM', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY');
    """
    connection.cursor().execute(sql)

def create_faux_ed_import_states(connection):
    sql = 'DROP TABLE IF EXISTS electoral_district_import CASCADE;'
    connection.cursor().execute(sql)
    sql = 'CREATE TABLE electoral_district_import as select identifier as id_long, id from electoral_district;'
    connection.cursor().execute(sql)

def pk_tables(table_dict, connection):
    for t in table_dict.values():
        sql, data = t.pk_sql_data()
        print sql.format(**data)
        connection.cursor().execute(sql.format(**data))
