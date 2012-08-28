import re, sys


LONG_TYPE = 'varchar(255)'
class field:
    def __init__(self, name, stype, default=None):
        self.name = name
        self.type = stype
        self.default = default
        self.long_from = False
        self.long_to = False

    def sql(self, long_fields=False):
        sql, data = self.sql_data(long_fields)
        return sql % data

    def sql_data(self, long_fields=False):
        if long_fields and self.long_to:
            return '%s %s%s,%s %s', (self.name, self.type, (' DEFAULT %s' % self.default) if self.default else '',self.name+'_long', LONG_TYPE)
        elif long_fields and self.long_from:
            return '%s %s', (self.name+'_long', LONG_TYPE)
        else:
            return '%s %s%s', (self.name, self.type, (' DEFAULT %s' % self.default) if self.default else '')

class table:
    t_re = re.compile(r'(?P<constraint>\s*CONSTRAINT\s+(?:"?(?P<cname>\w+)"?)\s+UNIQUE\s+\((?P<ckeys>(?:\s*"?\w+"?\s*,?\s*)+)\)\s*,?)|(?P<pk>\s*PRIMARY\s+KEY\s*\((?P<pkeys>(?:\s*"?\w+"?\s*,?\s*)+)\)\s*,?)|(?P<field>\s*"?(?P<fname>\w+)"?\s+(?P<type>\w+(?:\(\d+\))?)(?:\s+DEFAULT\s+(?P<default>\w+(?:\(\'\w+\'\))?))?,?)')
    create_re = re.compile(r'\s*CREATE\s+TABLE\s+"?(\w+)"?\s*\((.+)\)')
    field_re = re.compile(r'\s*"?(?P<name>\w+)"?\s+(?P<type>\w+)(?:\s+DEFAULT\s+(?P<default>.+))?')
    pk_re = re.compile(r'\s*PRIMARY\s+KEY\s*\((.+)\)')
    def __init__(self):
        self.name = None
        self.fields = {} #dict of field objects
        self.primary_keys = [] #list of tuples. A tuple with multiple entries is a primary key on more than one field
        self.constraints = [] #unique constraints

    def has_long(self):
        return any(f.long_from or f.long_to for f in self.fields.values())

    def sql_import(self, actual_table, name_override=None):
        return 'CREATE TABLE {name} ({fields});'.format(name=(actual_table['import_table']['table'] if not name_override else name_override), fields=','.join([f.sql() for f in self.fields.values()] + ['{name} text'.format(name=f['long']) for f in actual_table['long_fields']] ))

    def sql_fields(self, actual_table, prefix):
        return '{fields}'.format(fields=','.join([prefix+'_'+f.sql() for f in self.fields.values()] + ['{prefix}_{name} text'.format(prefix=prefix, name=f['long']) for f in actual_table['long_fields']]))

    def sql(self, long_fields=False, drop_keys=False):
        if long_fields:
            return 'CREATE TABLE %s_long (%s);' % (self.name, ','.join([f.sql(long_fields) for f in self.fields.values()]))
        else:
            return 'CREATE TABLE %s (%s);' % (self.name, ','.join([f.sql(long_fields) for f in self.fields.values()] + (['PRIMARY KEY (%s)' % (','.join(pk)) for pk in self.primary_keys] if not drop_keys else '') + [c.sql() for c in self.constraints]))

    def sql_data(self, long_fields=False, drop_keys=False):
        fsql = ','.join(f.sql_data(long_fields)[0] for f in self.fields.values())
        fdata = tuple(d for f in self.fields.values() for d in f.sql_data(long_fields)[1])
        if long_fields:
            return 'CREATE TABLE %%s_long (%s);' % fsql, (self.name,) + fdata
        else:
            csql = ','.join(c.sql_data()[0] for c in self.constraints)
            cdata = tuple(d for c in self.constraints for d in c.sql_data()[1])
            return 'CREATE TABLE %%s (%s);' % ','.join([fsql] + (['PRIMARY KEY (%s)' for pk in self.primary_keys] if not drop_keys else []) + ([csql] if csql else [])), (self.name,) + fdata + (tuple(','.join(pk) for pk in self.primary_keys)if not drop_keys else ()) + cdata

    def pk_sql_data(self, state, election):
        return 'ALTER TABLE {table_name}_{state}_{election} ADD PRIMARY KEY ({pk});', {'table_name':self.name, 'state':state,'election':election, 'pk':','.join(self.primary_keys[0])}

#NOTE ONLY HANDLES SINGLE FIELD FKS RIGHT NOW
    def rekey_imports(self, actual_table, rekey_table_dict, **split_keys):
        long_field_dict = dict([(a['long'],a['real']) for a in actual_table['long_fields']])
        sql = 'INSERT INTO {name}'.format(name=self.name) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_keys).format(**split_keys)
        sql += '(' + ','.join([f.name for f in self.fields.values() if not f.name in long_field_dict.values()] + [long_field_dict[a['local_key']] for a in actual_table['long_to']] + [long_field_dict[a] for a in actual_table['long_from']]) +')'
        sql += ' SELECT ' + ','.join(['fromtable.{name}'.format(name=f.name) for f in self.fields.values() if not f.name in long_field_dict.values()] + ['totable{i}.{to_key} as {from_key}'.format(i=i, to_key=actual_table['long_to'][i]['real_to_key'], from_key=long_field_dict[actual_table['long_to'][i]['local_key']]) for i in range(len(actual_table['long_to']))] + ['fromtable.{name}'.format(name=long_field_dict[a]) for a in actual_table['long_from']])
        sql += ' from {rekey_table_name}'.format(rekey_table_name=actual_table['rekey_table_name'] if actual_table.has_key('rekey_table_name') else actual_table['import_table']['table']) + ' as fromtable '
        sql += ''.join(' left join {name}'.format(name=rekey_table_dict[actual_table['long_to'][i]['to_table']]) + ' as totable{i} on '.format(i=i) + 'lower(fromtable.{from_key}) = lower(totable{i}.{to_key})'.format(i=i,from_key=actual_table['long_to'][i]['local_key'],to_key=actual_table['long_to'][i]['to_key']) for i in range(len(actual_table['long_to'])))+';\n'
        return sql

    def rekey_insert(self, fks, **split_keys):
        fks = [fk for fk in fks if fk.table == self.name]
        sql = 'INSERT INTO {name}'.format(name=self.name) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_keys).format(**split_keys) 
        sql += '(' + ','.join([f.name for f in self.fields.values() if not f.long_from and not f.long_to] + [a for fk in fks for a in fk.reference_fields])
        sql += ') SELECT ' + ','.join('fromtable.{name}'.format(name=f.name) for f in self.fields.values() if not f.long_from and not f.long_to) 
        sql +=(',' if len(fks) > 0 and len([f for f in self.fields.values() if not f.long_from and not f.long_to]) else '') 
        sql +=','.join('totable{i}.{to_key} as {from_key}'.format(i=i,to_key=fk.reference_fields[a],from_key=a) for i,fk in zip(range(len(fks)),fks) for a in fk.reference_fields) 
        sql += ' from {name}_long'.format(name=self.name) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_keys).format(**split_keys) + ' as fromtable' 
        sql += ''.join(' left join {name}_long'.format(name=fk.reference_table) + ''.join('_{{{sk}}}'.format(sk=sk) for sk in split_keys).format(**split_keys) + ' as totable{i} on '.format(i=i) + ' and '.join('fromtable.{from_key}_long = totable{i}.{to_key}_long'.format(i=i,from_key=a,to_key=fk.reference_fields[a]) for a in fk.reference_fields) for i,fk in zip(range(len(fks)),fks))+';\n'
        data = [self.name] + [f.name for f in self.fields.values() if not f.long_from and not f.long_to] + [a for b in [[i, fks[i].reference_fields[fks[i].reference_fields.keys()[j]], fks[i].reference_fields.keys()[j]] for i in range(len(fks)) for j in range(len(fks[i].reference_fields))] for a in b] + [self.name] + [a for b in [[fks[i].reference_table,i] + [c for d in [[fks[i].reference_fields.keys()[j],i,fks[i].reference_fields[fks[i].reference_fields.keys()[j]]] for j in range(len(fks[i].reference_fields))] for c in d] for i in range(len(fks))] for a in b]
        return sql, tuple(data)

    def rekey(self, fks):
        sql = 'CREATE TABLE %s as SELECT ' + ','.join('fromtable.%s' for f in self.fields.values() if not f.long_from and not f.long_to) +(',' if len(fks) > 0 and len([f for f in self.fields.values() if not f.long_from and not f.long_to]) else '') +','.join('totable%s.%s as %s' for fk in fks for a in fk.reference_fields) + ' from %s_long as fromtable' + ''.join(' left join %s_long as totable%s on ' + ' and '.join('fromtable.%s_long = totable%s.%s_long' for a in fk.reference_fields) for fk in fks)+';\n'
        data = [self.name] + [f.name for f in self.fields.values() if not f.long_from and not f.long_to] + [a for b in [[i, fks[i].reference_fields[fks[i].reference_fields.keys()[j]], fks[i].reference_fields.keys()[j]] for i in range(len(fks)) for j in range(len(fks[i].reference_fields))] for a in b] + [self.name] + [a for b in [[fks[i].reference_table,i] + [c for d in [[fks[i].reference_fields.keys()[j],i,fks[i].reference_fields[fks[i].reference_fields.keys()[j]]] for j in range(len(fks[i].reference_fields))] for c in d] for i in range(len(fks))] for a in b]
        return sql, tuple(data)

class fk_constraint:
    fk_alter_re = re.compile(r'\s*ALTER\s+TABLE\s+?"(?P<from_table>\w+)"?\s+ADD\s+CONSTRAINT\s+(?:"?(?P<name>\w+)"?\s+)FOREIGN\s+KEY\s+\((?P<froms>.+)\)\s+REFERENCES\s+"?(?P<to_table>\w+)"?\s+\((?P<tos>.+)\)')
    def __init__(self):
        self.table = None #table that the constraint is on
        self.name = None #possibly empty name of constraint
        self.reference_table = None #table the key relates TO
        self.reference_fields = {} #dict of keys in from table to keys in to table

class unique_constraint:
    unique_re = re.compile(r'\s*CONSTRAINT\s+(?:"?(?P<name>\w+)"?)\s+UNIQUE\s+\((?P<fields>.+)\)')
    def __init__(self):
        self.table = None #table that the constraint is on
        self.name = None #possibly empty name of constraint
        self.fields = () #tuple of fields which must together be unique

    def sql(self):
        return 'CONSTRAINT%s UNIQUE (%s)' % (' '+self.name if self.name else '', ','.join(self.fields))

    def sql_data(self):
        return 'CONSTRAINT%s UNIQUE (%s)', (' '+self.name if self.name else '', ','.join(self.fields))

class enum:
    enum_re = re.compile(r'\s*CREATE\s+TYPE\s+"?(\w+)"?\s+AS\s+ENUM\s+\((.+)\)')
    def __init__(self):
        self.name = None #enum name
        self.choices = () #possible enum values

class seq:
    seq_re = re.compile(r'\s*CREATE\s+SEQUENCE\s+"?(\w+)"?\s+START\s+(\d+)\s*')
    def __init__(self):
        self.name = None #sequence name
        self.start = 1 #beginning of sequence

blank_re = re.compile(r'^\s*$')
choice_re = re.compile(r',?[\'"]?(\w+)[\'"]?')

def split_no_parens(string, delimiter=','):
    split = string.split(',')
    ret_split = []
    i = 0
    while i < len(split):
        s = split[i]
        ret_split.append(s)
        if s.count('(') > s.count(')'):
            while ret_split[-1].count('(') != s.count(')') and i != len(split)-1:
                i+=1
                s = split[i]
                ret_split[-1] += ','+s
        i+=1
    return ret_split

def objectify_statement(statement, tables, enums, fks, seqs):
    m = enum.enum_re.match(statement)
    if m:
        e = enum()
        e.name = m.groups()[0]
        e.choices = tuple(n.groups()[0] for n in choice_re.finditer(m.groups()[1]))
        enums.append(e)
        return
    m = seq.seq_re.match(statement)
    if m:
        s = seq()
        s.name = m.groups()[0]
        s.start = int(m.groups()[1])
        seqs.append(s)

    m = fk_constraint.fk_alter_re.match(statement)
    if m:
        fk = fk_constraint()
        if m.groupdict().has_key('name'):
            fk.name = m.groupdict()['name']
        fk.table = m.groupdict()['from_table']
        fk.reference_table = m.groupdict()['to_table']
        fk.reference_fields = dict(zip((n.groups()[0] for n in choice_re.finditer(m.groupdict()['froms'])), (n.groups()[0] for n in choice_re.finditer(m.groupdict()['tos']))))
        fks.append(fk)
        return
    m = table.create_re.match(statement)
    if m:
        t = table()
        t.name = m.groups()[0]
        for n in table.t_re.finditer(m.groups()[1]):
            if n.groupdict()['pk']:
                t.primary_keys.append(tuple(o.groups()[0] for o in choice_re.finditer(n.groupdict()['pkeys'])))
            elif n.groupdict()['constraint']:
                uc = unique_constraint()
                uc.table = t.name
                uc.name = n.groupdict()['cname']
                uc.fields = tuple(o.groups()[0] for o in choice_re.finditer(n.groupdict()['ckeys']))
                t.constraints.append(uc)
            elif n.groupdict()['field']:
                t.fields[n.groupdict()['fname']] = field(n.groupdict()['fname'], n.groupdict()['type'], n.groupdict()['default'])
        """
        for s in split_no_parens(m.groups()[1]):
            m = table.pk_re.match(s.strip())
            if m:
                t.primary_keys.append(tuple(n.groups()[0] for n in choice_re.finditer(m.groups()[0])))
                continue
            m = unique_constraint.unique_re.match(s.strip())
            if m:
                uc = unique_constraint()
                uc.table = t.name
                if m.groupdict().has_key('name'):
                    uc.name = m.groupdict()['name']
                uc.fields = tuple(n.groups()[0] for n in choice_re.finditer(m.groups()[1]))
                t.constraints.append(uc)
                continue
            m = table.field_re.match(s.strip())
            if m:
                default = m.groupdict()['default'] if m.groupdict().has_key('default') else None
                t.fields.append(field(m.groupdict()['name'],m.groupdict()['type'],default))
                continue
        """
        tables[t.name] = t
        return

def rip_schema(schema_file_name):
    with open(schema_file_name,'r') as schema_file:
        tables = {}
        enums = []
        fks = []
        seqs = []
        statement = ''
        for l in schema_file:
            l = l.split('--')[0].strip()
            if blank_re.match(l):
                continue
            if ';' in l:
                l = l.split(';')
                for s in l[:-1]:
                    statement += ' '+s
                    objectify_statement(statement, tables, enums, fks, seqs)
                    statement = ''
                statement += ' '+l[-1]
            else:
                statement += ' '+l
        objectify_statement(statement, tables, enums, fks, seqs)
        return tables, enums, fks, seqs

if __name__=='__main__':
    tables, enums, fks, seqs = rip_schema(sys.argv[1])
    tdict = dict([(t.name, t) for t in tables])
    print tdict['electoral_district__precinct'].primary_keys
