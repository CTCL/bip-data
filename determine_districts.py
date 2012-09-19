import sys, csv, os, imp, time, subprocess
from collections import defaultdict

def main(state, remove = False):
    minim = 20
    maxim = 34
    shift = minim - 1
    state_conf = os.path.join(*['data','voterfiles',state,'state_conf.py'])
    state_conf = imp.load_source('state_conf', state_conf)
    vf_districts = dict([(k,v-1 - shift) for k,v in state_conf.VOTER_FILE['columns'].iteritems() if k in state_conf.VOTER_FILE_DISTRICTS])
    precincts = defaultdict(lambda:dict((k,defaultdict(lambda:0)) for k in vf_districts.keys()))
    district_entries = defaultdict(lambda:set())
    district_lists = defaultdict(lambda:[])
    vf_precincts = (
            ('county_number',state_conf.VOTER_FILE['columns']['county_number']-1 - shift),
            #('county_id',VOTER_FILE['columns']['county_id']-1),
            #('residential_city',VOTER_FILE['columns']['residential_city']-1),
            #('township', VOTER_FILE['columns']['township']-1),
            ('precinct_code',state_conf.VOTER_FILE['columns']['precinct_code']-1 - shift),
            ('precinct_name',state_conf.VOTER_FILE['columns']['precinct_name']-1 - shift))
    county_idx = state_conf.VOTER_FILE['columns']['county_id']-1 - shift
    if not os.path.exists(state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION):
        pipe = subprocess.Popen(['unzip',state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION.replace('.txt','.zip'), '-d', os.path.split(os.path.abspath(state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION))[0]],stdin=subprocess.PIPE)
        pipe.wait()
    t = time.time()
    pipe = subprocess.Popen(['cut','-f','{min}-{max}'.format(min=minim,max=maxim),state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION],stdout=subprocess.PIPE)
    cut_location = state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION.replace('.txt','.cut')
    with open(cut_location,'w') as f:
        f.writelines(pipe.stdout)
    print 'cutting time: {t}'.format(t=(time.time() - t))

    with open(cut_location,'r') as f, open(os.path.join(*[state_conf.VOTER_FILE_LOCATION]),'w') as g:
        csvr = csv.reader(f, delimiter=state_conf.VOTER_FILE['field_sep'])
        csvw = csv.writer(g, delimiter=state_conf.VOTER_FILE['field_sep'])
        csvw.writerow(csvr.next())
        x = 1
        t = time.time()
        time1 = 0
        time2 = 0
        time3 = 0
        precinct_ed = set()
        for line in csvr:
            precinct_code = tuple(line[i] for n,i in vf_precincts)
            peds =[]
            write_flag=False
            for k,v in vf_districts.iteritems():
                val = line[v]
                if val == '':
                    continue
                if k == 'county_council':
                    ed = line[county_idx] + ' ' + val
                    district_entries[k].add(ed)
                else:
                    ed = val
                    district_entries[k].add(ed)
                precincts[precinct_code][k][ed] += 1
                if not write_flag and precincts[precinct_code][k][ed] == 1:
                    precinct_ed.add(precinct_code + (k,ed))
                    write_flag=True
                #peds.append(precinct_code + (k,ed))
            #if len(precinct_ed.intersection(peds)) < len(peds):
            #    precinct_ed.update(peds)
            #    csvw.writerow(line)
            if write_flag:
                csvw.writerow(line)
            if x % 100000 == 0:
                print "{state}, {count}, {time}".format(state=state,count=x, time=time.time() - t)
                #print "time1: {0}, time2: {1}, time3: {2}".format(time1,time2,time3)
                time1 = 0
                time2 = 0
                time3 = 0
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
        for k in vf_districts.keys():
            v = district_entries[k]
            lv = list(v)
            lv.sort()
            g.write("{district} = {values}\n".format(district=k, values=lv))
    if remove:
        pipe = subprocess.Popen(['rm',state_conf.UNCOMPRESSED_VOTER_FILE_LOCATION],stdin=subprocess.PIPE)
        pipe.wait()
    pipe = subprocess.Popen(['rm',cut_location],stdin=subprocess.PIPE)
    pipe.wait()

if __name__=='__main__':
    state = sys.argv[1].lower()
    main(state)
