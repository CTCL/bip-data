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
