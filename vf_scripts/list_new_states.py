import os, re, sys
import script_settings as ss
os.chdir(ss.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir('/home/gaertner/Dropbox/BIP Production') if re.match(r'\w\w Candidates.csv',d)]
old = os.listdir('/home/gaertner/Dropbox/BIP Production/candidate_to_ed_tables')
has_data = []
for d in l:
    if d not in cands or d in old:
        continue
    q = os.listdir(d)
    for t in q:
        if re.match(r'TS_Google.*\.txt',t) or re.match(r'vf_compressed',t):
            #if re.match(r'TS_Google.*\.txt',t) and d in cands:
            has_data.append(d)
            break
has_data.sort()
print ','.join(has_data)

