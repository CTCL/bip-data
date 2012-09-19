import os, re, csv, imp, sys
os.chdir('../voterfiles')
if 'debug' in sys.argv:
    debug = True
else:
    debug = False
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
search_states = l
if len(sys.argv) > 1:
    search_states = sys.argv[1].split(',')
for d in l:
    if d not in search_states:
        continue
    q = os.listdir(d)
    os.chdir('../..')
    sys.path.append('.')
    imp.load_source('state_conf',os.path.join('data','voterfiles',d,'state_conf.py'))
    ed_map = imp.load_source('ed_map',os.path.join('data','voterfiles',d,'ed_map.py')).ed_map
    os.chdir('data/voterfiles')
    for t in q:
        if t == 'out':
            for s in os.listdir(os.path.join(d,t)):
                if s == 'contest.csv':
                    with open(os.path.join(d,t,s),'r') as f:
                        print 'PROCESSING {d}'.format(d=d)
                        csvr = csv.DictReader(f)
                        for n in csvr:
                            if n['electoral_district_id'] == '':
                                if debug:
                                    import pdb; pdb.set_trace()
                                print '{state} no map for {name}  ed_map result: {ed}'.format(state=d,name=n['electoral_district_name'], ed=(ed_map[n['electoral_district_name']] if ed_map.has_key(n['electoral_district_name']) else 'no entry'))
