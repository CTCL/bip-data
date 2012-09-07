import os, re
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir('/home/gaertner/Dropbox/BIP Production') if re.match(r'\w\w Candidates.csv',d)]
has_data = []
for d in l:
    q = os.listdir(d)
    for t in q:
        if re.match(r'TS_Google.*\.txt',t):
            #if re.match(r'TS_Google.*\.txt',t) and d in cands:
            has_data.append(d)
has_data.sort()
print ','.join(has_data)

