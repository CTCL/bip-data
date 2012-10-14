import os, re, csv
import sys
import imp
from collections import defaultdict, namedtuple
import time
import script_settings as ss
os.chdir(ss.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
header = ['state','congressional_district','state_representative_district','state_senate_district','judicial_district','school_district','county_council','county_id']
os.chdir(ss.home)
sys.path.append('.')
with open(os.path.join(ss.script_home,'precinct_report.csv'),'w') as pre_rep:
    minim = 20
    maxim = 34
    shift = minim - 1
    shift = 0
    csv_pre_rep = csv.writer(pre_rep)
    csv_pre_rep.writerow(['state_name','total'] + header + ['maxfrac {type}'.format(type=h) for h in header])
    for state in l:
        state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
        state_conf = imp.load_source('state_conf', state_conf)
        vf_districts = dict([(k,v-1-shift) for k,v in state_conf.VOTER_FILE['columns'].iteritems() if k in state_conf.VOTER_FILE_DISTRICTS])
        precincts = defaultdict(lambda:dict((k,defaultdict(lambda:0)) for k in vf_districts.keys()))
        vf_precincts = (
                ('county_number',state_conf.VOTER_FILE['columns']['county_number']-1-shift),
                #('county_id',VOTER_FILE['columns']['county_id']-1),
                #('residential_city',VOTER_FILE['columns']['residential_city']-1),
                #('township', VOTER_FILE['columns']['township']-1),
                ('precinct_code',state_conf.VOTER_FILE['columns']['precinct_code']-1-shift),
                ('precinct_name',state_conf.VOTER_FILE['columns']['precinct_name']-1-shift))
        county_idx = state_conf.VOTER_FILE['columns']['county_id']-1 - shift
        with open(os.path.join(*[state_conf.VOTER_FILE_LOCATION]),'r') as f:
            csvr = csv.reader(f, delimiter=state_conf.VOTER_FILE['field_sep'])
            csvr.next()
            for line in csvr:
                precinct_code = tuple(line[i] for n,i in vf_precincts)
                for k,v in vf_districts.iteritems():
                    val = line[v]
                    if line[v] == '':
                        continue
                    if k == 'county_council':
                        ed = line[county_idx] + ' ' + val
                    else:
                        ed = val
                    precincts[precinct_code][k][ed] += 1
            num_undet = defaultdict(lambda:0)
            max_frac = defaultdict(lambda:[0,0])
            for k,v in precincts.iteritems():
                if any([len(l) > 1 for l in v.values()]):
                    for l,m in v.iteritems():
                        if len(m) > 1:
                            max_frac[l][0] += max(m.values())
                            max_frac[l][1] += sum(m.values())
                            num_undet[l] += 1
            csv_pre_rep.writerow([state,len(precincts)] + [num_undet[k] for k in header] + [((float(max_frac[l][0])/float(max_frac[l][1])) if max_frac[l][1] > 0 else 1) for l in header])
