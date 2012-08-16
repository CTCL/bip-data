import sys
import csv
import os
import re
from collections import defaultdict, OrderedDict
from patterns import named_zip
geo_sequence = 1

def _remove_columns(file_name, remove_list):
    out_name = file_name+'.cut'
    with open(file_name) as infile:
        columns = infile.readline().strip().split(',')
        idxs = tuple(columns.index(r) for r in remove_list)
    with open(out_name, 'w') as outfile, open(file_name) as infile:
        csvw = csv.writer(outfile)
        csvw.writerows(cutcsv(infile, remove_list, idxs))
    return out_name

def cutcsv(infile, columns_to_remove, column_idxs=None):
    reader = csv.reader(infile)
    header = reader.next()
    if not column_idxs:
        column_idxs = [header.index(c) for c in columns_to_remove]
    yield [header[i] for i in range(len(header)) if i not in column_idxs]
    for row in reader:
        yield [row[i] for i in range(len(row)) if i not in column_idxs]

def convert_to_long(table_name, file_name, relations_from, relations_to, extra_long_keys, remove_keys=[], rename_keys={}):
    if len(remove_keys) > 0:
        file_name = _remove_columns(file_name,remove_keys)
    with open(file_name, 'r') as f:
        header = f.readline().strip().split(',')
        header_map = passdict([(key, key+'_long') for key in relations_from] + [(key, key+'_long') for key in relations_to] + [(key, key+'_long') for key in extra_long_keys])
        rename_map = passdict(rename_keys)
        sql = 'COPY %s(' + ','.join(['%s' for h in header]) + ') from \'%s\' CSV HEADER;\n'
        data = [table_name + '_long'] + [header_map[rename_map[h]] for h in header] + [file_name]
    return sql % tuple(data)

def convert_addresses(table_name, file_name, relations_from, relations_to, extra_long_keys, remove_keys=[], rename_keys={}):
    with open(file_name, 'r') as in_file, open(file_name+'.cons', 'w') as consaddy_file, open(file_name+'.addy', 'w') as geo_address_file:
        csvr = csv.reader(in_file)
        csvgw = csv.writer(geo_address_file)
        csvw = csv.writer(consaddy_file)
        header = csvr.next()
        ididx = header.index('id')
        address_fields = (tuple(header[i].split('.')) + (i,)  for i in range(len(header)) if 'address.' in header[i])
        addresses = defaultdict(lambda: OrderedDict())
        for k1,k2,i in address_fields:
            addresses[k1][k2] = i
        csvgw.writerow(addresses.values()[0].keys() + ['id','zip4'])
        naidx = [i for i in range(len(header)) if 'address.' not in header[i]]
        consaddyhead = [header[i] for i in naidx] + [a for a in addresses]
        csvw.writerow(consaddyhead)
        global geo_sequence
        for row in csvr:
            narow = [row[i] for i in naidx]
            for k1 in addresses:
                zips = named_zip.match(row[addresses[k1]['zip']])
                if zips != None:
                    zips = dict(((k,v) for k,v in zips.groupdict().iteritems() if v != None and k in ['zip','zip4']))
                    row[addresses[k1]['zip']] = zips['zip']
                else:
                    zips = defaultdict(lambda: '')
                csvgw.writerow([row[i] for i in addresses[k1].values()] + [geo_sequence, zips.get('zip4', '')])
                narow.append(geo_sequence)
                geo_sequence += 1
            csvw.writerow(narow)
    sql = convert_to_long(table_name, file_name+'.cons', relations_from, relations_to, extra_long_keys, remove_keys, rename_keys)
    sql += convert_to_long('geo_address', file_name+'.addy', {}, ('id',), [], remove_keys, rename_keys)
    return sql

def convert_street_segment(table_name, file_name, relations_from, relations_to, extra_long_keys, remove_keys=[], rename_keys={}):
    with open(file_name, 'r') as ss_file, open(file_name+'.cons', 'w') as ss_cons_file, open(file_name+'.addy', 'w') as ss_addy_file:
        ss_reader = csv.reader(ss_file)
        ss_no_addy_writer = csv.writer(ss_cons_file)
        ss_addys_writer = csv.writer(ss_addy_file)
        header = ss_reader.next()
        nha_cols = [(i,header[i].replace('nha_','')) for i in range(len(header)) if 'nha_' in header[i]]
        non_nha_cols = [(i, header[i]) for i in range(len(header)) if 'nha_' not in header[i]]
        ididx = header.index('id')
        ss_addys_writer.writerow([h for (i,h) in nha_cols] + ['id'])
        ss_no_addy_writer.writerow([h for (i,h) in non_nha_cols] + ['non_house_address'])
        global geo_sequence
        for row in ss_reader:
            ss_addys_writer.writerow([row[i] for (i,h) in nha_cols] + [geo_sequence])
            r = [row[i] for (i,h) in non_nha_cols] + [geo_sequence]
            ss_no_addy_writer.writerow(r)
            geo_sequence+=1
    sql = convert_to_long(table_name,file_name+'.cons', relations_from, relations_to, extra_long_keys, remove_keys, rename_keys)
    sql += convert_to_long('geo_address',file_name+'.addy', {}, ('id',), [], remove_keys, rename_keys)
    return sql

copy_statement_functions = defaultdict(lambda:convert_to_long, {'street_segment':convert_street_segment, 'polling_location':convert_addresses, 'election_administration':convert_addresses})

remove_keys = defaultdict(lambda:list(), {'state':['election_administration_id', 'early_vote_site_id'],'locality':['election_administration_id', 'early_vote_site_id'],'source':['feed_contact_id','tou_url']})
rename_keys = defaultdict(lambda:dict(), {'source':{'vip_id':'id'}})
#THIS IS UNNECESSARY IF THE DB FILES ARE CREATED WITH JOIN TABLES
extra_long_keys = defaultdict(lambda:list(), {'precinct':['polling_location_id']})

def create_table_sql(table):
    return '\n'.join([table[0]]+[str(n+' '+t) for (n,t) in table[1].iteritems()]+table[2]+[table[3]])

def rekey_sql(name, columns, relations, extra_long):
    sql = 'CREATE TABLE %s as select ' + ','.join('fromtable.%s' for c in columns if not c.endswith('_long'))
    sql += ',' if len(relations) > 0 and len([c for c in columns if not c.endswith('_long')]) > 0 else ''
    sql += ','.join('%s_long%s.%s as %s' for i in relations)
    sql += ',' if len(relations) >0 and len(extra_long) > 0 else ''
    sql += ','.join('fromtable.%s as %s' for i in extra_long) + '\n'
    sql += 'from %s_long as fromtable' + ' left join %s_long as %s_long%s on fromtable.%s_long = %s_long%s.%s_long'*len(relations)+';\n'
    data = [name] + [c for c in columns if not c.endswith('_long')]
    data+=[i for a in [[relations[key][0], j, relations[key][1],key] for (key,j) in zip(relations, range(len(relations)))] for i in a] + [i for a in [[key+'_long', key] for key in extra_long] for i in a]  + [name] + [i for a in [[relations[key][0], relations[key][0], j, key, relations[key][0], j, relations[key][1]] for (key,j) in zip(relations, range(len(relations)))] for i in a]
    return sql % tuple(data), sql, data

def do_rekey_sql(name, columns, relations, extra_long, db_conn):
    sql_data, sql, data = rekey_sql(name, columns, relations, extra_long)
    db_conn.cursor().execute(sql, data)

def table_statement_gen(first_line, schema_file):
    yield first_line
    n = schema_file.next()
    while ';' not in n:
        yield n
        n = schema_file.next()
    yield n

def parse_table_statement_std_format(lines):
    constraints=[]
    columns = dict()
    for l in lines:
        if "CREATE TABLE" in l:
            create_table=l.strip().split(' ')
            create_table[2] = create_table[2][1:-1] + '_long'
            create_table = ' '.join(create_table)
        elif "PRIMARY KEY" in l or "CONSTRAINT" in l:
            constraints.append(l.strip())
        elif ';' in l:
            end = l.strip()
        else:
            columns[l.split(' ')[0][1:-1]] = ' '.join(l.split(' ')[1:]).strip()
    return (create_table, columns, constraints, end)


class passdict(dict):
    def __missing__(self,key):
        return key

with open(sys.argv[1], 'r') as schema_file, open(sys.argv[2], 'w') as new_schema_file, open(sys.argv[3], 'w') as rekey_file, open(sys.argv[4],'w') as copy_file:
    if len(sys.argv) > 5:
        data_dir = sys.argv[5] 
    else:
        data_dir = '/var/bip/data/vip_feeds/vipFeed-39-2012-03-06.xml.flattened'
    table_files = os.listdir(data_dir)
    fks = []
    tables = dict()
    for line in schema_file:
        if "FOREIGN KEY" in line:
            fks.append(line.strip().split(' '))
        elif "CREATE TABLE" in line:
            tables[line.split(' ')[2][1:-1]] = parse_table_statement_std_format(table_statement_gen(line, schema_file))
        elif line !='\n':
            new_schema_file.write(line)

    fk = fks[0]
    from_idx = fk.index("TABLE") + 1
    key_idx = fk.index("KEY") + 1
    to_idx = fk.index("REFERENCES") + 1
    target_idx = len(fk)-1
    from_tables = defaultdict(lambda: defaultdict(lambda: dict()))
    to_tables = defaultdict(lambda:set())
    table_column_map = defaultdict(lambda:passdict())
    constraint_split = re.compile('[\(\)]')
    for fk in fks:
        from_tables[fk[from_idx][1:-1]][fk[key_idx][2:-2]] = (fk[to_idx][1:-1],fk[target_idx][2:-3])
        to_tables[fk[to_idx][1:-1]].add(fk[target_idx][2:-3])
    for table in from_tables:
        for key in from_tables[table]:
            tables[table][1].pop(key)
            tables[table][1][key+'_long'] = 'varchar(255),'
            table_column_map[table][key] = key+'_long'
    for table in to_tables:
        for key in to_tables[table]:
            tables[table][1][key+'_long'] = 'varchar(255),'
#            table_column_map[table][key] = key+'_long'
    for table in tables:
        for key in extra_long_keys[table]:
            tables[table][1].pop(key)
            tables[table][1][key+'_long'] = 'varchar(255),'
            table_column_map[table][key] = key+'_long'
        for j in range(len(tables[table][2])):
            c = tables[table][2][j]
            cs = constraint_split.split(c)
            constraint_fields = cs[1].split(',')
            for i in range(len(constraint_fields)):
                constraint_fields[i] = table_column_map[table][constraint_fields[i].strip()[1:-1]]
            tables[table][2][j] = cs[0] + '(' + ','.join(constraint_fields) + ')' + cs[2]
        new_schema_file.write(create_table_sql(tables[table]) + '\n\n')
        rekey_file.write(rekey_sql(table, tables[table][1].keys(),from_tables[table], extra_long_keys[table]))
        table_file = data_dir + os.sep + table+'.txt'
        if os.path.exists(table_file):
            #This can take a while, since it regenerates split address files TODO make regeneration of files a separate function
            copy_file.write(copy_statement_functions[table](table,table_file,from_tables[table], to_tables[table], extra_long_keys[table], remove_keys[table], rename_keys[table]))
