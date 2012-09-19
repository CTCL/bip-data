import subprocess, os, re, sys
os.chdir('../voterfiles')

dir_list = [f for f in os.listdir('.') if re.match(r'^[a-z][a-z]$',f)]
state_list = dir_list
if len(sys.argv) > 1:
    state_list = sys.argv[1].split(',')

for f in dir_list:
    if f not in state_list:
        continue
    os.chdir(f)
    zips = [g for g in os.listdir('.') if '.zip' in g and 'TS_Google' in g]
    txts = [g for g in os.listdir('.') if '.txt' in g]
    for g in zips:
        if g.replace('.zip','.txt') in txts:
            continue
        pipe = subprocess.Popen(['unzip',g],stdin=subprocess.PIPE)
        pipe.wait()
    os.chdir('..')
