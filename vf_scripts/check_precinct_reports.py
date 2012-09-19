import os, re, csv
import sys
import imp
from collections import defaultdict, namedtuple
import time
import script_settings as ss
from quartiles import quartiles
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
    csv_pre_rep.writerow(['state_name','total precincts'] + header + ['frac bad {type}'.format(type=h) for h in header] + ['maxfrac {type}'.format(type=h) for h in header] + [q for h in header for q in 'min {type},1st {type},med {type},3rd {type},max {type}'.format(type=h).split(',')])
    for state in l:
        state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
        state_conf = imp.load_source('state_conf', state_conf)
        vf_precincts = (
                ('county_number',state_conf.VOTER_FILE['columns']['county_number']-1-shift),
                #('county_id',VOTER_FILE['columns']['county_id']-1),
                #('residential_city',VOTER_FILE['columns']['residential_city']-1),
                #('township', VOTER_FILE['columns']['township']-1),
                ('precinct_code',state_conf.VOTER_FILE['columns']['precinct_code']-1-shift),
                ('precinct_name',state_conf.VOTER_FILE['columns']['precinct_name']-1-shift))
        with open(os.path.join(*[state_conf.VOTER_FILE_LOCATION]),'r') as f:
            csvr = csv.reader(f, delimiter=state_conf.VOTER_FILE['field_sep'])
            csvr.next()
            precincts = set()
            for line in csvr:
                precinct_code = tuple(line[i] for n,i in vf_precincts)
                precincts.add(precinct_code)
            total = len(precincts)
        num_undet = defaultdict(lambda:0)
        max_frac = defaultdict(lambda:[0,0])
        split_percents = defaultdict(lambda:[])
        with open(os.path.join(ss.voterfiles,state,'precincts'),'r') as f:
            pat = re.compile(r'POSSIBLE (?P<type>\w+) VALUES: (?P<tuples>\[.*\])')
            for l in f:
                l = l.split('\t')[:-1]
                undets = l.pop(0).split('UNDETERMINED: ')[1]
                for u in undets.split(','):
                    num_undet[u] += 1
                for entry in l:
                    m = pat.match(entry)
                    if not m:
                        import pdb;pdb.set_trace()
                    counts = [count for name, count in eval(m.groupdict()['tuples'])]
                    dist_type = m.groupdict()['type']
                    max_frac[dist_type][0] += max(counts)
                    max_frac[dist_type][1] += sum(counts)
                    split_percents[dist_type].append(float(max(counts))/float(sum(counts)))

        csv_pre_rep.writerow([state,len(precincts)] + [num_undet[k] for k in header] + ['{0:.5f}'.format(float(num_undet[k])/len(precincts)) for k in header] + [('{0:.5f}'.format(float(max_frac[l][0])/float(max_frac[l][1])) if max_frac[l][1] > 0 else 1) for l in header] + ['{0:.5f}'.format(q) for h in header for q in (quartiles(split_percents[h]))])
