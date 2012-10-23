import re
named_zip = re.compile(r'(?P<trash>[A-Z]*)(?P<zip>\d{5})-?(?P<zip4>\d{4})?')
x=0
debug = False
def address_seq():
    global x
    x+=1
    return str(x),

def zip_parse(z):
    m = named_zip.match(z)
    return m.groupdict()['zip'] if m.groupdict()['zip'] else '', m.groupdict()['zip4'] if m.groupdict()['zip4'] else ''

def create_vf_address(street_num, pre_dir, street_name, street_suf, post_dir, unit_des, apt_num):
    primary = [k for k in [street_num, pre_dir, street_name, street_suf, post_dir] if k and len(k)>0]
    secondary = [k for k in [unit_des, apt_num] if k and len(k)>0]
    return ' '.join(primary), ' '.join(secondary)

def concat_us(*args, **kwargs):
    return '_'.join(args + tuple(kwargs.values())),

def _saintrep(m):
    return m.groupdict()['prefix'] + 'st' + m.groupdict()['suffix']

def ed_concat(*args, **kwargs):
    name = concat_us(*args, **kwargs)[0]
    name = re.sub(r'(?P<prefix>[_\s]|^)s(?:ain)?te?\.?(?P<suffix>[_\s]|$)', _saintrep, name.lower().strip())
    name = name.replace("'",'')
    return name,

def referendum_id(state, referendum_title):
    return '{state}_{referendum_title}'.format(state=state.strip(), referendum_title=referendum_title.strip()).lower(),

def contest_id(state, district, office_name):
    return '{state}_{district}_{office_name}'.format(state=state.strip(), district=district.strip(), office_name=office_name.strip()).lower(),

#An issue here is that the electoral district map made for each state is
#created from the district names in the voterfile, so if these district
#names do not contain enough information to replicate the candidate file
#district names, a problem arises. The candidate file names need to be
#transformed to simpler forms that can be matched from the VF
#So we'll introduce a transform function
def get_edmap(map_location):
    import imp
    ed_map = imp.load_source('ed_map',map_location)
    class passdict(dict):
        def __missing__(self,key):
            return {'name':key,'type':''}
    ed_map = passdict(ed_map.ed_map)
    patt = re.compile(r'(?P<name>\D+)(?P<number>\d+)(?P<extra>\D?)$')

    def edmap(electoral_district):
        electoral_district = ' '.join(re.split(r'\s+',electoral_district.strip()))
        print electoral_district
        m = patt.match(electoral_district)
        if m:
            electoral_district = '{name}{number}{extra}'.format(name=m.groupdict()['name'], number=int(m.groupdict()['number']), extra=m.groupdict()['extra'])
        #TODO this regex has problems with 2 saints next to each other
        electoral_district = re.sub(r'(?P<prefix>[_\s]|^)s(?:ain)?te?\.?(?P<suffix>[_\s]|$)', _saintrep, electoral_district.lower().strip())
        electoral_district = electoral_district.replace("'",'')
        print electoral_district
        if not ed_map.has_key(electoral_district):
            #import pdb;pdb.set_trace()
            pass
        t = ed_map[electoral_district]
        print t
        if debug and not ed_map.has_key(electoral_district):
            import pdb;pdb.set_trace()
        return t['name'],t['type'], ed_concat(t['name'],t['type'])[0], ed_map.has_key(electoral_district)
    return edmap
