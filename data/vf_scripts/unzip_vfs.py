import subprocess, os, re
os.chdir('../voterfiles')

dir_list = [f for f in os.listdir('.') if re.match(r'^[a-z][a-z]$',f)]

for f in dir_list:
    os.chdir(f)
    zips = [g for g in os.listdir('.') if '.zip' in g and 'TS_Google' in g]
    txts = [g for g in os.listdir('.') if '.txt' in g]
    for g in zips:
        if g.replace('.zip','.txt') in txts:
            continue
        pipe = subprocess.Popen(['unzip',g],stdin=subprocess.PIPE)
        pipe.wait()
    os.chdir('..')
