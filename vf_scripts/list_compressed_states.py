import os, re, sys
if '-strict' in sys.argv:
    strict = True
else:
    strict = False
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
cands = [re.match(r'(?P<state>\w\w) Candidates.csv', d).groupdict()['state'].lower() for d in os.listdir('/home/gaertner/Dropbox/BIP Production') if re.match(r'\w\w Candidates.csv',d)]
has_compressed = []
no_compressed = []
for d in l:
    if d not in cands and strict:
        continue
    q = os.listdir(d)
    if os.path.exists(os.path.join(d,'vf_compressed')):
        #if re.match(r'TS_Google.*\.txt',t) and d in cands:
        has_compressed.append(d)
    else:
        no_compressed.append(d)
has_compressed.sort()
print 'compressed: ' + ','.join(has_compressed)
print 'uncompressed: ' + ','.join(no_compressed)

