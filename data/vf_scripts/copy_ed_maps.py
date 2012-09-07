import os, re
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
has_data = []
for d in l:
    q = os.listdir(d)
    for t in q:
        if re.match(r'TS_Google.*\.zip',t):
            with open('/home/gaertner/bip_data/vf_scripts/ed_map_template.py','r') as h, open(os.path.join(d,'ed_map.py'),'w') as j:
                for n in h:
                    j.write(n)
            break
