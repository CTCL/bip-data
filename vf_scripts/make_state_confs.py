import os, re
import script_settings
os.chdir(script_settings.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir(script_settings.candidates) if re.match(r'\w\w Candidates.csv',d)]
print cands
has_data = set()
for d in l:
    q = os.listdir(d)
    for t in q:
        #        print os.path.join(d,t)
        if (re.match(r'TS_Google.*\.txt',t) or re.match(r'vf_compressed',t))  and d in cands:
            has_data.add(d)
        if re.match(r'TS_Google.*\.zip',t):
            conf_file = os.path.join(script_settings.script_home,'exception_states','state_conf_template_{state}.py'.format(state=d))
            if not os.path.exists(conf_file):
                conf_file = os.path.join(script_settings.script_home,'state_conf_template.py')
            ed_map_file = os.path.join(script_settings.script_home,'exception_states','ed_map_template_{state}.py'.format(state=d))
            if not os.path.exists(ed_map_file):
                ed_map_file = os.path.join(script_settings.script_home,'ed_map_template.py')
            with open(conf_file,'r') as f, open(os.path.join(d,'state_conf.py'),'w') as g, open(ed_map_file,'r') as h, open(os.path.join(d,'ed_map.py'),'w') as j, open(os.path.join(d,'__init__.py'),'w') as m:
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

