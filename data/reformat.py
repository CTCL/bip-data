import re
named_zip = re.compile(r'(?P<trash>[A-Z]*)(?P<zip>\d{5})-?(?P<zip4>\d{4})?')
x=0
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

def contest_id(state, district, office_name):
    return '{state}_{district}_{office_name}'.format(state=state.strip(), district=district.strip(), office_name=office_name.strip()).lower(),

def get_edmap(map_location):
    import imp
    ed_map = imp.load_source('ed_map',map_location)
    ed_map = ed_map.ed_map
    def edmap(electoral_district):
        t = ed_map[electoral_district.lower().strip()]
        return t['name'],t['type'], '{name}_{type}'.format(**t)
    return edmap
