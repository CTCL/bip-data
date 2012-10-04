"""
UNCOMPRESSED_VOTER_FILE_LOCATION is, of course, the path to the actual voterfile
minim and maxim define the column range you want. Of course you can replace this with an explicit comma separated list of columns. One weird thing I've noticed about cut is that no matter what order you list those in, it will keep them in the order they are in in the original file, so cut -f 5,4 returns the same as cut -f 4,5
"""
import time, subprocess
t = time.time()
pipe = subprocess.Popen(['cut','-f','{min}-{max}'.format(min=minim,max=maxim),state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION],stdout=subprocess.PIPE)
cut_location = state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION.replace('.txt','.cut')
with open(cut_location,'w') as f:
    f.writelines(pipe.stdout)
print 'cutting time: {t}'.format(t=(time.time() - t))
