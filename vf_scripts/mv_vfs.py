import subprocess, os, re
os.chdir('../voterfiles')

dir_list = [f for f in os.listdir('.') if 'TS_Google' in f]

for f in dir_list:
    print f
    m = re.match(r'.*_(?P<state>[A-Z][A-Z])_.*',f)
    d = m.groupdict()['state'].lower()
    pipe = subprocess.Popen(['mv',f,d],stdin=subprocess.PIPE)
    pipe.wait()
