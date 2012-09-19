import os, re
import script_settings
os.chdir(script_settings.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
has_data = []
for d in l:
    q = os.listdir(d)
    for t in q:
        if re.match(r'TS_Google.*\.zip',t):
            ed_map_file = os.path.join(script_settings.script_home,'exception_states','ed_map_template_{state}.py'.format(state=d))
            if not os.path.exists(ed_map_file):
                ed_map_file = os.path.join(script_settings.script_home,'ed_map_template.py')
            with open(ed_map_file,'r') as h, open(os.path.join(d,'ed_map.py'),'w') as j:
                for n in h:
                    j.write(n)
            break
