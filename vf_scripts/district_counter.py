import os, re, imp, csv
import script_settings
os.chdir(script_settings.voterfiles)
l = [d for d in os.listdir('.') if re.match(r'^\w\w$',d)]
header = ['state','congressional_district','state_rep_district','state_senate_district','judicial_district','school_district','county_council','county_id']
with open(os.path.join(script_settings.script_home, 'missing_districts.csv'),'w') as f, open(os.path.join(script_settings.script_home, 'district_counts.csv'),'w') as g:
    csv_f = csv.writer(f)
    csv_g = csv.writer(g)
    csv_f.writerow(['state_name'] + header)
    csv_g.writerow(['state_name'] + header)
    for d in l:
        q = os.listdir(d)
        for t in q:
            if t == 'districts.py':
                districts = imp.load_source('districts',os.path.join(d,t))
                csv_g.writerow([d] + [len(districts.__dict__[e]) for e in header])
                #if any([len(districts.__dict__[e]) == 0 for e in header]):
                csv_f.writerow([d] + [('x' if len(districts.__dict__[e]) == 0  else '') for e in header])
                break
