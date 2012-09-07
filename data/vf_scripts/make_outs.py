import os, re
os.chdir('../voterfiles')
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
has_data = []
for d in l:
    try:
        os.mkdir(os.path.join(d,'out'))
    except:
        pass
    os.chmod(os.path.join(d,'out'),511)

