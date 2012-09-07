import re
import csv
from data.state_specific import districts
from districts import *

intpat = re.compile(r'^\d+$')

ed_map = {}
ed_map.update(dict([('{state} Congressional District {number}'.format(state=state[0], number=(int(n) if intpat.match(n) else n)).lower(),{'name':n,'type':'congressional_district'}) for n in congressional_district]))
ed_map.update({state[0].lower():{'name':state[0].lower(), 'type':'state'}})
ed_map.update(dict([('{name} County'.format(name=name).lower(),{'name':name,'type':'county'}) for name in county_id]))
ed_map.update(dict([('{state} State Senate District {number}'.format(state=state[0], number=(int(n) if intpat.match(n) else n)).lower(),{'name':n,'type':'state_senate_district'}) for n in state_senate_district]))
ed_map.update(dict([('{state} State House District {number}'.format(state=state[0], number=(int(n) if intpat.match(n) else n)).lower(),{'name':n,'type':'state_rep_district'}) for n in state_representative_district]))

county_council = []
for county in county_council:
    m =  re.match(r'(?P<county_name>\D+)\s(?P<district_number>\d{2})?', county)
    if m.groupdict()['district_number']:
        county_council.append(('{county_name} County District {district_number}'.format(**m.groupdict()).lower(),{'name':'{county_name}_{district_number}'.format(**m.groupdict()),'type':'county_council'}))
        county_council.append(('{county_name} County District {district_number}'.format(county_name=m.groupdict()['county_name'],district_number=int(m.groupdict()['district_number'])).lower(),{'name':'{county_name}_{district_number}'.format(**m.groupdict()),'type':'county_council'}))
ed_map.update(dict(county_council))

if __name__ == '__main__':
    print ed_map
