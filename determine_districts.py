import sys
import csv
import os
import imp
from collections import defaultdict, namedtuple
import time

def main(state):
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    vf_districts = dict([(k,v-1) for k,v in state_conf.VOTER_FILE['columns'].iteritems() if k in state_conf.VOTER_FILE_DISTRICTS])
    precincts = defaultdict(lambda:dict((k,defaultdict(lambda:0)) for k in vf_districts.keys()))
    district_entries = defaultdict(lambda:set())
    vf_precincts = (
            ('county_number',state_conf.VOTER_FILE['columns']['county_number']-1),
            #('county_id',VOTER_FILE['columns']['county_id']-1),
            #('residential_city',VOTER_FILE['columns']['residential_city']-1),
            #('township', VOTER_FILE['columns']['township']-1),
            ('precinct_code',state_conf.VOTER_FILE['columns']['precinct_code']-1),
            ('precinct_name',state_conf.VOTER_FILE['columns']['precinct_name']-1))
    with open(state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION,'r') as f, open(os.path.join(*[state_conf.VOTER_FILE_LOCATION]),'w') as g:
        csvr = csv.reader(f, delimiter=state_conf.VOTER_FILE['field_sep'])
        csvw = csv.writer(g, delimiter=state_conf.VOTER_FILE['field_sep'])
        csvw.writerow(csvr.next())
        x = 1
        t = time.time()
        precinct_ed = set()
        for line in csvr:
            precinct_code = tuple(line[i] for n,i in vf_precincts)
            for k,v in vf_districts.iteritems():
                if line[v] == '':
                    continue
                precincts[precinct_code][k][line[v]] += 1
                if k == 'county_council':
                    ed = line[state_conf.VOTER_FILE['columns']['county_id']-1] + ' ' + line[v]
                    district_entries[k].add(line[state_conf.VOTER_FILE['columns']['county_id']-1] + ' ' + line[v])
                else:
                    ed = line[v]
                    district_entries[k].add(line[v])
            ped = precinct_code + (ed,)
            if ped not in precinct_ed:
                precinct_ed.add(ped)
                csvw.writerow(line)
            if x % 100000 == 0:
                print len(precincts)
                print sys.getsizeof(district_entries)
                print sys.getsizeof(precincts)
                print "{count}, {time}".format(count=x, time=time.time() - t)
                t = time.time()
            x+=1
    with open(os.path.join(*['data','voterfiles',state,'precincts']),'w') as f, open(os.path.join(*['data','voterfiles',state,'districts.py']),'w') as g, open(os.path.join('data','voterfiles',state,'counts.csv'),'w') as h, open(os.path.join('data','voterfiles',state,'names.csv'),'w') as namesfile:
        print "TOTAL PRECINCTS: {precincts}".format(precincts=len(precincts))
        csvh = csv.writer(h)
        csvnames = csv.writer(namesfile)
        csvh.writerow(['precinct','district type','d1','d2','d3','d4','d5','etc'])
        csvnames.writerow(['precinct','district type','d1','d2','d3','d4','d5','etc'])
        num_undet = defaultdict(lambda:0)
        for k,v in precincts.iteritems():
            if any([len(l) > 1 for l in v.values()]):
                f.write("{precinct} HAS UNDETERMINED: {districts}\t".format(precinct=k, districts=','.join(l for l in v.keys() if len(v[l]) > 1)))
                for l,m in v.iteritems():
                    if len(m) > 1:
                        num_undet[l] += 1
                        f.write("POSSIBLE {district} VALUES: {values}\t".format(district=l, values=[(distk,distv) for distk,distv in m.iteritems()]))
                        distnames = []
                        distcounts = []
                        for distk,distv in m.iteritems():
                            distnames.append(distk)
                            distcounts.append(str(distv))
                        csvh.writerow([k,l] + distcounts)
                        csvnames.writerow([k,l] + distnames)
                f.write('\n')
        for k,v in num_undet.iteritems():
            print "NUM PRECINCTS WITH UNDETERMINED {district}: {num}".format(district=k, num=v)
        for k,v in district_entries.iteritems():
            lv = list(v)
            lv.sort()
            g.write("{district} = {values}\n".format(district=k, values=lv))

if __name__=='__main__':
    state = sys.argv[1].lower()
    main(state)
