import os, re
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
has_data = []
for d in l:
    q = os.listdir(d)
    for t in q:
        if t == 'precincts':
            with open(os.path.join(d,t),'r') as f:
                for n in f:
                    print '%s %s' % (d,n)
