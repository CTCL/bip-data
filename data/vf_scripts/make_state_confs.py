import os, re
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir('/home/gaertner/Dropbox/BIP Production') if re.match(r'\w\w Candidates.csv',d)]
has_data = []
for d in l:
    q = os.listdir(d)
    for t in q:
        print os.path.join(d,t)
        if re.match(r'TS_Google.*\.txt',t) and d in cands:
            has_data.append(d)
        if re.match(r'TS_Google.*\.zip',t):
            with open('/home/gaertner/bip_data/vf_scripts/state_conf_template.py','r') as f, open(os.path.join(d,'state_conf.py'),'w') as g, open('/home/gaertner/bip_data/vf_scripts/ed_map_template.py','r') as h, open(os.path.join(d,'ed_map.py'),'w') as j open(os.path.join(d,'__init__.py'),'w') as m:
                k.write('county_id = []\n')
                k.write('county_council = []\n')
                k.write('state_representative_district = []\n')
                k.write('state_senate_district = []\n')
                k.write("state = ['{state}']\n".format(state=d))
                k.write('congressional_district = []\n')
                for n in h:
                    j.write(n)
                for n in f:
                    if 'state_specific.STATE' in n:
                        g.write(n.replace('NJ',d.upper()))
                    elif 'state_specific.UNCOMPRESSED_VOTER_FILE_LOCATION' in n:
                        g.write(n.replace('example',os.path.abspath(os.path.join(d,t.replace('.zip','.txt')))))
                    else:
                        g.write(n)
print ','.join(has_data)

