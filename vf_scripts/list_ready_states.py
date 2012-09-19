import os, re, sys
import script_settings as ss
if '-strict' in sys.argv:
    strict = True
else:
    strict = False
os.chdir(ss.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir('/home/gaertner/Dropbox/BIP Production') if re.match(r'\w\w Candidates.csv',d)]
has_data = []
for d in l:
    if d not in cands and strict:
        continue
    q = os.listdir(d)
    for t in q:
        if re.match(r'TS_Google.*\.txt',t) or re.match(r'vf_compressed',t):
            #if re.match(r'TS_Google.*\.txt',t) and d in cands:
            has_data.append(d)
            break
has_data.sort()
print ','.join(has_data)

