from jinja2 import Template
import csv, os
import script_settings as ss

def make_char(dist_type):
    with open('precinct_report.csv','r') as f, open(os.path.join(ss.script_home,'charts',dist_type+'.html'),'w') as g:
        data = []
        template = Template(open(os.path.join(ss.script_home,'chart_templates','candlestick_dict.html'),'r').read())
        csvr = csv.DictReader(f)
        for line in csvr:
            data.append({'idx':csvr.line_num-2,'count':float(line[dist_type])/float(line['total']),'min':line['min {t}'.format(t=dist_type)],'third':line['1st {t}'.format(t=dist_type)],'first':line['3rd {t}'.format(t=dist_type)],'max':line['max {t}'.format(t=dist_type)],'state':line['state_name']})
        g.write(template.render(data=data))

if __name__ == '__main__':
    make_char('congressional_district')
    make_char('state_representative_district')
    make_char('state_senate_district')
    make_char('judicial_district')
    make_char('school_district')
    make_char('county_council')
