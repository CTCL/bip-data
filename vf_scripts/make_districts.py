import os, re, sys
import script_settings as ss
os.chdir(ss.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir(ss.candidates) if re.match(r'\w\w Candidates.csv',d)]
has_data = []
state_picks = l
if len(sys.argv) > 1:
    state_picks = sys.argv[1].split(',')
for d in l:
    if d not in state_picks:
        continue
    q = os.listdir(d)
    for t in q:
        print os.path.join(d,t)
        if re.match(r'TS_Google.*\.txt',t) and d in cands:
            has_data.append(d)
        if re.match(r'TS_Google.*\.zip',t):
            with open(os.path.join(d,'districts.py'),'w') as k:
                k.write('county_id = []\n')
                k.write('county_council = []\n')
                k.write('state_representative_district = []\n')
                k.write('state_senate_district = []\n')
                k.write("state = ['{state}']\n".format(state=d))
                k.write('congressional_district = []\n')
                k.write('ward = []\n')
