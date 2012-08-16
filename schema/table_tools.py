
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

def pk_tables(table_dict, connection):
    for t in table_dict.values():
        sql, data = t.pk_sql_data()
        print sql.format(**data)
        connection.cursor().execute(sql.format(**data))
