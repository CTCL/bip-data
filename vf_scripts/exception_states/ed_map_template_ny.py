import re
import csv
import data.state_specific as ss
from data.reformat import _saintrep
ss = reload(ss)
districts = ss.districts 
from collections import defaultdict
d_dict = defaultdict(lambda:[],districts.__dict__)
judicial_district = d_dict['judicial_district']
county_council = d_dict['county_council']
congressional_district = d_dict['congressional_district']
state_senate_district = d_dict['state_senate_district']
state_representative_district = d_dict['state_rep_district']
school_district = d_dict['school_district']
county_school_district = d_dict['county_school_district']
county_id = d_dict['county_id']
city_council = d_dict['city_council']
special_judicial_district = d_dict['special_1_judicial_district']
state = districts.state

intpat = re.compile(r'^(?P<number>\d+)(?P<extra>\D*)$')
jdpat = re.compile(r'^(?:JD)?(?P<number>\d+)(?P<extra>\D*)$')
sdpat = re.compile(r'^(?:S[DS])?(?P<number>\d+)$')
def numberclean(n):
    m = intpat.match(n)
    if m:
        return str(int(m.groupdict()['number'])) + m.groupdict()['extra']
    else:
        return n

ed_map = {}
ed_map.update({state[0].lower():{'name':state[0].lower(), 'type':'state'}})
ed_map.update(dict([('{state} Judicial District Supreme Court Supreme Court {number}'.format(state=state[0], number=(numberclean(jdpat.match(n).groupdict()['number']+jdpat.match(n).groupdict()['extra']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'special_1_judicial_district'}) for n in special_judicial_district]))

ed_map.update(dict([('{state} Congressional District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'congressional_district'}) for n in congressional_district]))
ed_map.update(dict([('{state} State Senate District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_senate_district'}) for n in state_senate_district]))
ed_map.update(dict([('{state} State House District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State House of Representatives - District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State Representative District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State Legislature District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} Legislative District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} Judicial District {number}'.format(state=state[0], number=(numberclean(jdpat.match(n).groupdict()['number']+jdpat.match(n).groupdict()['extra']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'judicial_district'}) for n in judicial_district]))
ed_map.update(dict([('{state} District Court - District {number}'.format(state=state[0], number=(numberclean(jdpat.match(n).groupdict()['number']+jdpat.match(n).groupdict()['extra']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'judicial_district'}) for n in judicial_district]))
ed_map.update(dict([('{state} State School Board District {number}'.format(state=state[0], number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('{state} Board of Education District {number}'.format(state=state[0], number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('{state} State Board of Education District {number}'.format(state=state[0], number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))

ed_map.update(dict([('Congressional District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'congressional_district'}) for n in congressional_district]))
ed_map.update(dict([('State Senate District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'state_senate_district'}) for n in state_senate_district]))
ed_map.update(dict([('State House District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State House of Representatives - District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('State Representative District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('State Legislature District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('Legislative District {number}'.format(number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('Judicial District {number}'.format(number=(numberclean(jdpat.match(n).groupdict()['number']+jdpat.match(n).groupdict()['extra']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'judicial_district'}) for n in judicial_district]))
ed_map.update(dict([('State School Board District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('Board of Education District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('State Board of Education District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))

def county_name_clean(county):
    county = re.sub(r'(?P<prefix>[_\s]|^)s(?:ain)?te?\.?(?P<suffix>[_\s]|$)', _saintrep, county.lower().strip())
    county = county.replace("'",'')
    return county

for county in county_id:
    county = county_name_clean(county)
    ed_map.update({'{name} County'.format(name=county).lower():{'name':county,'type':'county'}})
    if county.endswith('city'):
        ed_map.update({'{name}'.format(name=county).lower():{'name':county,'type':'county'}})

roman_map = {'I':1,'II':2,'III':3,'IV':4,'V':5,'i':1,'ii':2,'iii':3,'iv':4,'v':5}
def clean_county_number(district_number):
    try:
        return int(district_number)
    except:
        return roman_map[district_number]
sd_fillers = ('county school board district','county school board','school board district', 'school board' 'county school board precinct','school board precinct','school district','school precinct','county - school board district','county - school board', 'county board of education','board of education','county board of education district','board of education district','county - board of education district')
sd_dicts = []
if ss.COUNTY_SCHOOL_DISTRICT:
    for sd in county_school_district:
        county_possibles = []
        for c in county_id:
            if sd.startswith(c):
                county_possibles.append(c)
        if county_possibles == []:
            continue
        county_name = max(county_possibles, key=len)
        old_sd = sd
        sd = county_name_clean(sd)
        old_county_name = county_name
        county_name = county_name_clean(county_name)
        old_district_stuff = old_sd.replace(old_county_name,'').strip()
        district_stuff = sd.replace(county_name,'').strip()
        if re.match(r'^\d+$', district_stuff):
            for f in sd_fillers:
                sd_dicts.append(('{county_name} {filler} {district_number}'.format(filler=f,county_name=county_name, district_number=clean_county_number(district_stuff)).lower(),{'name':'{county_name}_{district_stuff}'.format(county_name=old_county_name, district_stuff=old_district_stuff),'type':'school_district'}))
for sd in school_district:
    if re.match(r'^\d+$', sd):
        for f in sd_fillers:
            sd_dicts.append(('{filler} {district_number}'.format(filler=f, district_number=clean_county_number(sd)).lower(),{'name':'{district_stuff}'.format(district_stuff=sd),'type':'school_district'}))
ed_map.update(dict(sd_dicts))
county_council_dicts = []
fillers = ('County Commissioner Precinct','County Commission Precinct','County Comissioner District','Commissioner District', 'County Commissioner', 'CO Commission District','CO Commissioner District','County District','County Commissioner District','County - Commission District','County Commission District','County Committee District','County - Commissioner District','County - Comm District','County - Council District','County Council District','County - County Commissioner District','County - District','County Board District','County Board - District','- District', 'Commission District', '- County Commissioner District', 'County - County Commissioner - District')
for county in county_council:
    county_possibles = []
    for c in county_id:
        if county.startswith(c):
            county_possibles.append(c)
    if county_possibles == []:
        continue
    county_name = max(county_possibles, key=len)
    county = county_name_clean(county)
    county_name = county_name_clean(county_name)
    district_stuff = county.replace(county_name,'').strip()
    m = re.match(r'\D*(?P<district_number>[0-9]+)\D*',county)
    if not m:
        p = re.compile(r'.*\s(?P<district_number>[IViv]+)')
        m = p.match(county)
        if not (m and all(map(lambda s:p.match(county_name_clean(s)),[c for c in county_council if c.startswith(county_name.upper())]))):
            m = None
    for f in fillers:
        if m and  m.groupdict()['district_number']:
            county_council_dicts.append(('{county_name} {filler} {district_number}'.format(filler=f,county_name=county_name, district_number=clean_county_number(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{district_stuff}'.format(county_name=county_name, district_stuff=district_stuff),'type':'county_council'}))
        elif district_stuff.endswith('LRG'):
            county_council_dicts.append(('{county_name} {filler}'.format(filler=f,county_name=county_name).lower(),{'name':'{county_name}_{district_stuff}'.format(county_name=county_name, district_stuff=district_stuff),'type':'county_council'}))
        elif re.match(r'\w+\s\w',county):
            county_council_dicts.append(('{county_name} {filler} {district_letters}'.format(filler=f,county_name=county_name, district_letters=district_stuff.split(' ')[-1]).lower(),{'name':'{county_name}_{district_stuff}'.format(county_name=county_name, district_stuff=district_stuff),'type':'county_council'}))
        else:
            county_council_dicts.append(('{county_name} {filler} {district_letters}'.format(filler=f,county_name=county_name, district_letters=district_stuff).lower(),{'name':'{county_name}_{district_stuff}'.format(county_name=county_name, district_stuff=district_stuff),'type':'county_council'}))


ed_map.update(dict(county_council_dicts))

ed_map.update(dict(('new york (muni) city council district {number}'.format(number=numberclean(c)),{'name':c,'type':'city_council'}) for c in city_council))
if __name__ == '__main__':
    print ed_map
