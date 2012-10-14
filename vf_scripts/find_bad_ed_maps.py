import os, re, csv, imp, sys
import script_settings as ss
os.chdir(ss.voterfiles)
if 'debug' in sys.argv:
    debug = True
else:
    debug = False
if 'trim' in sys.argv:
    sys.argv.pop(1)
    trim = True
else:
    trim = False
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
search_states = l
if len(sys.argv) > 1:
    search_states = sys.argv[1].split(',')
os.chdir(ss.home)
sys.path.append('.')
imp.load_source('default_state_stuff',os.path.join('data','default_state_stuff.py'))
os.chdir(ss.voterfiles)
judicial_words = ['court','appeals','supreme','judicial']
school_words = ['school','education']
county_comm_words = ['commissioner','commission','district','committee','comm','council']

for d in l:
    if d not in search_states:
        continue
    q = os.listdir(d)
    os.chdir(ss.home)
    sys.path.append('.')
    imp.load_source('state_conf',os.path.join('data','voterfiles',d,'state_conf.py'))
    ed_map_mod = imp.load_source('ed_map',os.path.join('data','voterfiles',d,'ed_map.py'))
    ed_map = ed_map_mod.ed_map
    os.chdir('data/voterfiles')
    if len(ed_map_mod.county_council) == 0:
        no_county_council = True
    else:
        no_county_council = False
    if len(ed_map_mod.school_district) == 0:
        no_school_district = True
    else:
        no_school_district = False
    if len(ed_map_mod.judicial_district) == 0:
        no_judicial_district = True
    else:
        no_judicial_district = False
    sdsk = False
    jdsk = False
    ccsk = False
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
                                edn = n['electoral_district_name']
                                if trim:
                                    if no_school_district and any(map(lambda sn:sn in edn,school_words)):
                                        sdsk = True
                                        continue
                                    if no_judicial_district and any(map(lambda sn:sn in edn,judicial_words)):
                                        jdsk = True
                                        continue
                                    if no_county_council and any(map(lambda sn:sn in edn and 'county' in edn,county_comm_words)):
                                        ccsk = True
                                        continue
                                print '{state} no map for {name}  ed_map result: {ed}'.format(state=d,name=n['electoral_district_name'], ed=(ed_map[n['electoral_district_name']] if ed_map.has_key(n['electoral_district_name']) else 'no entry'))
                        if sdsk:
                            print 'school skipped'
                        if jdsk:
                            print 'judicial skipped'
                        if ccsk:
                            print 'county council skipped'
