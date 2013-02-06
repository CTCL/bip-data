import subprocess
import time
import csv
import sys
minim = 20
maxim = 34
vf_location = sys.argv[1]
#vf_location = '/home/gaertner/bip-data/data/voterfiles/wy/TS_Google_Geo_102912_WY_20121023.txt'
t = time.time()
pipe = subprocess.Popen(['cut','-f','1,{min}-{max}'.format(min=minim,max=maxim),vf_location],stdout=subprocess.PIPE)
cut_location1 = vf_location.replace('.txt','.cut1')
with open(cut_location1,'w') as f:
    f.writelines(pipe.stdout)
print 'cutting time: {t}'.format(t=(time.time() - t))

t = time.time()
cut_location2 = vf_location.replace('.txt','.cut2')
with open(vf_location) as f, open(cut_location2,'w') as g:
    csvf = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    csvg = csv.writer(g, delimiter='\t', quoting=csv.QUOTE_NONE)
    map(lambda r: csvg.writerow([r[0]] + r[19:34]), csvf)
    print 'cutting time: {t}'.format(t=(time.time() - t))

t = time.time()
cut_location3 = vf_location.replace('.txt','.cut3')
with open(vf_location) as f, open(cut_location3,'w') as g:
    csvf = csv.reader(f, delimiter='\t')
    csvg = csv.writer(g, delimiter='\t')
    map(lambda r: csvg.writerow([r[0]] + r[19:34]), csvf)
    print 'cutting time: {t}'.format(t=(time.time() - t))

pipe = subprocess.Popen(['diff','--strip-trailing-cr',cut_location1, cut_location2],stdout=subprocess.PIPE)
print pipe.stdout.read()
pipe = subprocess.Popen(['diff','--strip-trailing-cr',cut_location1, cut_location3],stdout=subprocess.PIPE)
print pipe.stdout.read()
