import re
import csv
import data.state_specific as ss
from data.reformat import _saintrep
ss = reload(ss)
districts = ss.districts
#township_to_district = ss.ttod
from collections import defaultdict
d_dict = defaultdict(lambda:[],districts.__dict__)
judicial_district = d_dict['judicial_district']
county_council = d_dict['county_council']
congressional_district = d_dict['congressional_district']
state_senate_district = d_dict['state_senate_district']
state_representative_district = d_dict['state_rep_district']
#state_representative_district += (list(set(township_to_district.t_d.values())))
school_district = d_dict['school_district']
county_id = d_dict['county_id']
township = d_dict['township']
floaterial = d_dict['special_1_state_rep_district']
state = districts.state

intpat = re.compile(r'^(?P<number>\d+)(?P<extra>\D?)$')
jdpat = re.compile(r'^(?:JD)?(?P<number>\d+)$')
sdpat = re.compile(r'^(?:S[DS])?(?P<number>\d+)$')
def numberclean(n):
    m = intpat.match(n)
    if m:
        return str(int(m.groupdict()['number'])) + m.groupdict()['extra']
    else:
        return n
sr_abbr_dict = dict((cid[:2],cid) for cid in county_id)
srpat = re.compile(r'^(?P<name>[A-Za-z ]+)-?(?P<number>\d+)(?:\D*)$')
def staterepclean(n):
    m = srpat.match(n)
    matched_counties = []
    for cid in county_id:
        if cid.startswith(m.groupdict()['name']):
            matched_counties.append(cid)
    name = max(matched_counties, key=len)
    #if sr_abbr_dict.has_key(m.groupdict()['name']):
        #name = sr_abbr_dict[m.groupdict()['name']]
    #else:
        #name = m.groupdict()['name'].strip()
    number = int(m.groupdict()['number'])
    return {'name':name,'number':number}

ed_map = {}
ed_map.update({state[0].lower():{'name':state[0].lower(), 'type':'state'}})


ed_map.update(dict([('{state} State House -{name} district {number}'.format(state=state[0], **staterepclean(n)).lower(),{'name':n,'type':'special_1_state_rep_district'}) for n in floaterial]))
ed_map.update(dict([('{state} State House -{name} district {number}'.format(state=state[0], **staterepclean(n)).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))

ed_map.update(dict([('{state} Congressional District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'congressional_district'}) for n in congressional_district]))
ed_map.update(dict([('{state} State Senate District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_senate_district'}) for n in state_senate_district]))
ed_map.update(dict([('{state} State House District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State House of Representatives - District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State Representative District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} State Legislature District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} Legislative District {number}'.format(state=state[0], number=(numberclean(n))).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))
ed_map.update(dict([('{state} Judicial District {number}'.format(state=state[0], number=(int(jdpat.match(n).groupdict()['number']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'judicial_district'}) for n in judicial_district]))
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
ed_map.update(dict([('Judicial District {number}'.format(number=(int(jdpat.match(n).groupdict()['number']) if jdpat.match(n) else n)).lower(),{'name':n,'type':'judicial_district'}) for n in judicial_district]))
ed_map.update(dict([('State School Board District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('Board of Education District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))
ed_map.update(dict([('State Board of Education District {number}'.format(number=(int(sdpat.match(n).groupdict()['number']) if sdpat.match(n) else n)).lower(),{'name':n,'type':'school_district'}) for n in school_district]))

ed_map.update(dict([('{name} township'.format(name=n).lower(), {'name':n,'type':'township'}) for n in township]))

for county in county_id:
    county = re.sub(r'(?P<prefix>[_\s]|^)s(?:ain)?t.?(?P<suffix>[_\s]|$)', _saintrep, county.lower().strip())
    county = county.replace("'",'')
    ed_map.update({'{name} County'.format(name=county).lower():{'name':county,'type':'county'}})

county_council_dicts = []
for county in county_council:
    county = re.sub(r'(?P<prefix>[_\s]|^)s(?:ain)?t.?(?P<suffix>[_\s]|$)', _saintrep, county.lower().strip())
    county = county.replace("'",'')
    m =  re.match(r'(?P<county_name>\D+)\s(?P<prefixed>(?:[Cc][Cc])?(?P<district_number>\d+)?)', county)
    if m and  m.groupdict()['district_number']:
        county_council_dicts.append(('{county_name} County District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County Commissioner District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County Commissioner District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Commission District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Commission District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Commissioner District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Commissioner District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Comm District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Comm District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Council District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))

        county_council_dicts.append(('{county_name} County - Council District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{prefixed}'.format(**m.groupdict()),'type':'county_council'}))
ed_map.update(dict(county_council_dicts))

if __name__ == '__main__':
    print ed_map
