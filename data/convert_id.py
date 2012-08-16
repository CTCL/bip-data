import sys
import csv
import time

class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self
    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

with open(sys.argv[1],'r') as rfile, open(sys.argv[2],'w') as wfile, Timer() as t:
    csvr = csv.reader(rfile)
    csvw = csv.writer(wfile)

    header = csvr.next()
    ididx = header.index('id')
    csvw.writerow(header)
    for row in csvr:
        row[ididx] = ''.join([str(ord(c)) for c in row[ididx]])
        csvw.writerow(row)
print 'time to execute: ' + str(t.interval)
