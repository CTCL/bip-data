import re, sys

class field:
    def __init__(self, name, stype, default=None):
        self.name = name
        self.type = stype
        self.default = default

class table:
    t_re = re.compile(r'(?P<constraint>\s*CONSTRAINT\s+(?:"?(?P<cname>\w+)"?)\s+UNIQUE\s+\((?P<ckeys>.+)\)\s*,?)|(?P<pk>\s*PRIMARY\s+KEY\s*\((?P<pkeys>.+)\)\s*,?)|(?P<field>\s*"?(?P<fname>\w+)"?\s+(?P<type>\w+)(?:\s+DEFAULT\s+(?P<default>.+))?,?)')
    create_re = re.compile(r'\s*CREATE\s+TABLE\s+"?(\w+)"?\s*\((.+)\)')
    field_re = re.compile(r'\s*"?(?P<name>\w+)"?\s+(?P<type>\w+)(?:\s+DEFAULT\s+(?P<default>.+))?')
    pk_re = re.compile(r'\s*PRIMARY\s+KEY\s*\((.+)\)')
    def __init__(self):
        self.fields = {} #dict of field objects
        self.primary_keys = [] #list of tuples. A tuple with multiple entries is a primary key on more than one field
        self.constraints = [] #unique and foreign key constraints

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
        if t.name == 'electoral_district__precinct':
            import pdb; pdb.set_trace()
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
                t.fields[n.groupdict()['fname'] = field(n.groupdict()['fname'], n.groupdict()['type'], n.groupdict()['default'])
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
                    objectify_statement(statement, tables, enums, fks)
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
