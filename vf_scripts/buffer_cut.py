import os, re, sys, subprocess
import script_settings as ss
os.chdir(ss.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
if len(sys.argv) > 1:
    l = [d for d in l if d in sys.argv[1].split(',')]
for d in l:
    if os.path.exists(os.path.join(d,'vf_compressed')):
        vfc = os.path.join(d,'vf_compressed')
        f = open(vfc)
        if f.next().startswith('\t'*19):
            f.close()
            continue
        else:
            f.close()
        vfcc = os.path.join(d,'vf_compressed_cut')
        pipe = subprocess.Popen(['mv',vfc,vfcc],stdin=subprocess.PIPE)
        pipe.wait()
        with open(os.path.join(d,'vf_compressed_cut'),'r') as f, open(os.path.join(d,'vf_compressed'),'w') as g:
            for l in f:
                g.write('\t'*19 + l)
