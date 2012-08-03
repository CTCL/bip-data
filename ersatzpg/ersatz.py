from collections import defaultdict
from cStringIO import StringIO
import psycopg2.psycopg1 as psycopg
import re, imp, csv, sys, time

def parse_config(config_file):
    with open(config_file, 'r') as cf:
        universal_config_dict = {'reformat_path':None, 'debug': False}
        table_config_dict = defaultdict(lambda: {'copy_every':100000, 'format':'csv','field_sep':',','quotechar':'"'})
        def parse_table_conf(tconf, tdict):
            for l in tconf:
                if l.startswith('#'): continue
                if re.match(r'\}', l):
                    if not tdict.has_key('table') or not tdict.has_key('filename') or not tdict.has_key('columns'):
                        raise Exception('table config must contain table, filename, and columns')
                    return tdict
                m = re.match(r'(\w+)\s*=\s*(.+)', l)
                if m:
                    tdict.update([m.groups()])
            if not tdict.has_key('table') or not tdict.has_key('filename') or not tdict.has_key('columns'):
                raise Exception('table config must contain table, filename, and columns')
            return tdict
        for l in cf:
            if l.startswith('#'): continue
            m = re.match(r'(\w+)\s*\{', l)
            if m:
                table_config_dict[m.groups()[0]] = parse_table_conf(cf, table_config_dict[m.groups()[0]])
            else:
                m = re.match(r'(\w+)\s*=\s*(.+)', l)
                if m:
                    universal_config_dict.update([m.groups()])
    if not universal_config_dict.has_key('user') or not universal_config_dict.has_key('db') or not universal_config_dict.has_key('pw'):
        raise Exception('config must contain user, db, and pw for postgres db')
    return universal_config_dict, table_config_dict

def db_connect(config):
    connstr = []
    if config.has_key('host'):
        connstr.append("host=%s" % config['host'])
    if config.has_key('port'):
        connstr.append("port=%s" % config['port'])
    if config.has_key('sslmode'):
        connstr.append("sslmode=%s" % config['sslmode'])
    connstr.append("dbname=%s user=%s password=%s" % (config['db'], config['user'], config['pw']))
    return psycopg.connect(' '.join(connstr))

def process_columns(table_conf, default_reformat_path):
    r_path = table_conf['reformat_path'] if table_conf.has_key('reformat_path') else default_reformat_path
    columns = table_conf['columns'].split(',')
    numbered_columns = []
    transformed_columns = []
    for c in columns:
        c = c.strip()
        m = re.match(r'(\w+)\s*:\s*(\d+)', c)
        if m:
            numbered_columns.append((m.groups()[0], int(m.groups()[1]) - 1))
        else:
            m = re.match(r'(\w+(?:\s+\w+)*)\s*:\s*(\w+)\.(\w+)\((\d+(?:\s+\d+)*)\)', c)
            if m:
                transformed_columns.append((re.split(r'\s+', m.groups()[0]), function_lookup(m.groups()[1], m.groups()[2], r_path), [int(x) - 1 for x in re.split(r'\s+', m.groups()[3])]))
    udcs = [tuple(s.strip() for s in t.split(':')) for t in table_conf['udcs'].split(',')] if table_conf.has_key('udcs') else []
    return numbered_columns, transformed_columns, udcs

def function_lookup(module_name, func_name, reformat_path):
    module = imp.load_module(module_name, *imp.find_module(module_name, reformat_path))
    return module.__dict__[func_name]

def process_data(row, numbered_columns, transformed_columns,udcs):
    return [row[i] for name,i in numbered_columns] + [v for tr in transformed_columns for v in tr[1](*[row[i] for i in tr[2]])] + [i for name, i in udcs]

def process_table(table_conf, univ_conf, connection):
    numbered_columns, transformed_columns, udcs = process_columns(table_conf, univ_conf['reformat_path'])
    table_def = "%s(%s)" % (table_conf['table'],','.join([name for name, i in numbered_columns]+[n for names, f, i in transformed_columns for n in names] + [name for name, t in udcs]))
    force_not_null = force_not_null = 'FORCE NOT NULL ' + ','.join(s.strip() for s in table_conf['force_not_null'].split(',')) if table.conf.has_key('force_not_null') else ''
    sql = "COPY %s from STDOUT WITH CSV DELIMITER '%s' QUOTE '%s' %s" % (table_def, table_conf['field_sep'], table_conf['quotechar'], force_not_null)
    field_sep = table_conf['field_sep']
    copy_every = int(table_conf['copy_every'])
    cursor = connection.cursor()
    with open(table_conf['filename'], 'rb') as f:
        buf = StringIO()
        csvr = csv.reader(f)
        if table_conf.has_key('skip_head_lines'):
            shl = int(table_conf['skip_head_lines'])
            for i in range(shl):
                csvr.next()
        x = 0
        ptime = 0
        ctime = 0
        for l  in csvr:
            ptime -= time.time()
            try:
                buf.write(field_sep.join(process_data(l, numbered_columns, transformed_columns, udcs))+'\n')
            except Exception, error:
                if univ_conf['debug']:
                    import pdb; pdb.set_trace()
                else:
                    raise error
            ptime += time.time()
            x+=1
            if x % copy_every == 0:
                print "Copying %s lines" % copy_every
                buf.seek(0)
                try:
                    ctime -= time.time()
                    cursor.copy_expert(sql, buf)
                    ctime += time.time()
                except Exception, error:
                    if univ_conf['debug']:
                        import pdb; pdb.set_trace()
                    else:
                        raise error
                buf.close()
                print "Time spent on building buffer: %s" % ptime
                print "Time spent copying: %s" % ctime
                ptime = 0
                ctime = 0
                buf = StringIO()
        buf.seek(0)
        print "Copying %s lines" % (x % copy_every)
        ctime -= time.time()
        cursor.copy_expert(sql, buf)
        ctime += time.time()
        buf.close()
        print "Time spent on building buffer: %s" % ptime
        print "Time spent copying: %s" % ctime

def process_copies(config_file):
    universal_conf, table_confs = parse_config(config_file)
    connection = db_connect(universal_conf)
    for table in table_confs:
        process_table(table_confs[table], universal_conf, connection)

if __name__ == "__main__":
    process_copies(sys.argv[1])
