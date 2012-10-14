import os, re, sys
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
if len(sys.argv) > 1:
    l = [d for d in l if d in sys.argv[1].split(',')]
for d in l:
    if os.path.exists(os.path.join(d,'vf_compressed_cut')):
        with open(os.path.join(d,'vf_compressed_cut'),'r') as f, open(os.path.join(d,'vf_compressed'),'w') as g:
            for l in f:
                g.write('\t'*19 + l)
