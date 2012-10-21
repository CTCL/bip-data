from data import univ_settings
univ_settings = reload(univ_settings)
import os, imp
from data import state_specific
state_specific.STATE = 'NJ'
state_specific.ELECTION = 2012
state_specific.VIP_SOURCE = state_specific.STATE+'VIP'
state_specific.VF_SOURCE = state_specific.STATE+'VF'
state_specific.CANDIDATE_SOURCE = state_specific.STATE+'Candidates'
state_specific.VIP_FEED_LOCATION = '/tmp/temp'
state_specific.ED_MAP_LOCATION = '/home/gaertner/bip-data/data/voterfiles/{state}/ed_map.py'.format(state=state_specific.STATE.lower())
#state_specific.ED_MAP_CSV_LOCATION = '/home/gaertner/bip-data/data/voterfiles/nj/ed_map.csv'
state_specific.CANDIDATE_FILE_LOCATION = '/home/gaertner/Dropbox/BIP Production/{state} Candidates.csv'.format(state=state_specific.STATE)
state_specific.UNCOMPRESSED_VOTER_FILE_LOCATION = 'example' 
state_specific.VOTER_FILE_LOCATION = '/home/gaertner/bip-data/data/voterfiles/{state}/vf_compressed'.format(state=state_specific.STATE.lower())
state_specific.HOME = '/home/gaertner/bip-data/data/voterfiles/{state}'.format(state=state_specific.STATE.lower())
state_specific.VOTER_FILE_SCHEMA = '/home/gaertner/bip-data/schema/ts_voter_file.sql'
state_specific.districts = imp.load_source('districts',os.path.join('data','voterfiles',state_specific.STATE.lower(), 'districts.py'))
state_specific.STATE_EDMAP = univ_settings.table_functions.get_edmap(state_specific.ED_MAP_LOCATION)
state_specific.COUNTY_SCHOOL_DISTRICT = False
state_specific.COUNTY_JUDICIAL_DISTRICT = False
from data.state_specific import *
from data import target_smart_defaults as tsd
tsd = reload(tsd)
from data import candidate_defaults as cd
cd = reload(cd)
#VOTER_FILE = tsd.VOTER_FILE
VOTER_FILE_DISTRICTS = tsd.VOTER_FILE_DISTRICTS

LEGISLATIVE_DISTRICT_IMPORT = dict(tsd.td.DEFAULT_VF_TABLE)
LEGISLATIVE_DISTRICT_IMPORT['udcs'] = dict(tsd.td.DEFAULT_VF_TABLE['udcs'])
LEGISLATIVE_DISTRICT_IMPORT['udcs'].update({'type':'legislative_district'})
LEGISLATIVE_DISTRICT_IMPORT.update({
    'table':'electoral_district_ld_import',
    'columns':{
        #'id':{'key':'congressional_district'},
        'name':25,
        'identifier':{'function':tsd.td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'legislative_district'}},
        'id_long':{'function':tsd.td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'legislative_district'}}
        },
    })

LEGISLATIVE_DISTRICT_ACTUAL = dict(tsd.td.DEFAULT_ACTUAL_TABLE)
LEGISLATIVE_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':LEGISLATIVE_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

LEGISLATIVE_DISTRICT__PRECINCT_IMPORT = dict(tsd.td.DEFAULT_VF_TABLE)
LEGISLATIVE_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_ld_import',
    'filename':state_specific.VOTER_FILE_LOCATION,
    'columns':{
        'electoral_district_id_long':{'function':tsd.td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'legislative_district'}},
        'precinct_id_long':{'function':tsd.td.reformat.concat_us,'columns':(22,29,28)},
        },
    })

LEGISLATIVE_DISTRICT__PRECINCT_ACTUAL = dict(tsd.td.DEFAULT_ACTUAL_TABLE)
LEGISLATIVE_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':LEGISLATIVE_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_ld_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

COUNTY_COUNCIL_IMPORT = dict(tsd.td.DEFAULT_VF_TABLE)
COUNTY_COUNCIL_IMPORT['udcs'] = dict(tsd.td.DEFAULT_VF_TABLE['udcs'])
COUNTY_COUNCIL_IMPORT['udcs'].update({'type':'county_council'})
COUNTY_COUNCIL_IMPORT.update({
    'table':'electoral_district_cc_import',
    'columns':{
        #'id':{'key':'county_council'},
        'name':30,
        'identifier':{'function':tsd.td.reformat.ed_concat,'columns':(30,),'defaults':{'type':'county_council'}},
        'id_long':{'function':tsd.td.reformat.ed_concat,'columns':(30,),'defaults':{'type':'county_council'}}
        },
    })

COUNTY_COUNCIL_ACTUAL = dict(tsd.td.DEFAULT_ACTUAL_TABLE)
COUNTY_COUNCIL_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':COUNTY_COUNCIL_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

COUNTY_COUNCIL__PRECINCT_IMPORT = dict(tsd.td.DEFAULT_VF_TABLE)
COUNTY_COUNCIL__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_cc_import',
    'filename':state_specific.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'county_council'},
        'electoral_district_id_long':{'function':tsd.td.reformat.ed_concat,'columns':(30,),'defaults':{'type':'county_council'}},
        'precinct_id_long':{'function':tsd.td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

COUNTY_COUNCIL__PRECINCT_ACTUAL = dict(tsd.td.DEFAULT_ACTUAL_TABLE)
COUNTY_COUNCIL__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':COUNTY_COUNCIL__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_cc_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

ACTUAL_TABLES = (
        tsd.PRECINCT_ACTUAL,
        tsd.LOCALITY_ACTUAL,
        tsd.CONGRESSIONAL_DISTRICT_ACTUAL,
        LEGISLATIVE_DISTRICT_ACTUAL,
        tsd.JUDICIAL_DISTRICT_ACTUAL,
        tsd.SCHOOL_DISTRICT_ACTUAL, 
        COUNTY_COUNCIL_ACTUAL,
        tsd.COUNTY_ACTUAL,
        tsd.STATE_ACTUAL,
        #tsd.STATE_SENATE_DISTRICT_ACTUAL,
        tsd.CONGRESSIONAL_DISTRICT__PRECINCT_ACTUAL,
        LEGISLATIVE_DISTRICT__PRECINCT_ACTUAL,
        tsd.JUDICIAL_DISTRICT__PRECINCT_ACTUAL,
        tsd.SCHOOL_DISTRICT__PRECINCT_ACTUAL,
        COUNTY_COUNCIL__PRECINCT_ACTUAL,
        tsd.COUNTY__PRECINCT_ACTUAL,
        #tsd.STATE_SENATE_DISTRICT__PRECINCT_ACTUAL,
        tsd.STATE__PRECINCT_ACTUAL,
        cd.CANDIDATE_ACTUAL,
        cd.CONTEST_ACTUAL,
        cd.CANDIDATE_IN_CONTEST_ACTUAL,
        )

GROUPS = {
        #        'vf_group':TABLE_GROUP,
        }
ELECTORAL_DISTRICT_UNION = dict(tsd.ELECTORAL_DISTRICT_UNION)
ELECTORAL_DISTRICT_UNION['components'] = (
            'electoral_district_cd_import',
            'electoral_district_jd_import',
            'electoral_district_schd_import',
            'electoral_district_ld_import',
            'electoral_district_cc_import',
            'electoral_district_c_import',
            'electoral_district_s_import',
            )
UNIONS = (
        ELECTORAL_DISTRICT_UNION,
        )
ERSATZPG_CONFIG = dict(univ_settings.ERSATZPG_CONFIG)
ERSATZPG_CONFIG.update({
    'use_utf':True,
    'tables':{
        #        'voter_file':VOTER_FILE,
        'precinct':tsd.PRECINCT_IMPORT,
        'locality':tsd.LOCALITY_IMPORT,
        'congressional_district':tsd.CONGRESSIONAL_DISTRICT_IMPORT,
        'legislative_district':LEGISLATIVE_DISTRICT_IMPORT,
        'judicial_district':tsd.JUDICIAL_DISTRICT_IMPORT,
        'school_district':tsd.SCHOOL_DISTRICT_IMPORT,
        'county_council':COUNTY_COUNCIL_IMPORT,
        'county':tsd.COUNTY_IMPORT,
        'state':tsd.STATE_IMPORT,
        #'state_senate_district':tsd.STATE_SENATE_DISTRICT_IMPORT,
        'legislative_district__precinct':LEGISLATIVE_DISTRICT__PRECINCT_IMPORT,
        'congressional_district__precinct':tsd.CONGRESSIONAL_DISTRICT__PRECINCT_IMPORT,
        #'state_senate_district__precinct':tsd.STATE_SENATE_DISTRICT__PRECINCT_IMPORT,
        'judicial_district__precinct':tsd.JUDICIAL_DISTRICT__PRECINCT_IMPORT,
        'school_district__precinct':tsd.SCHOOL_DISTRICT__PRECINCT_IMPORT,
        'county_council__precinct':COUNTY_COUNCIL__PRECINCT_IMPORT,
        'county__precinct':tsd.COUNTY__PRECINCT_IMPORT,
        'state__precinct':tsd.STATE__PRECINCT_IMPORT,
        'candidate':cd.CANDIDATE_IMPORT,
        'contest':cd.CONTEST_IMPORT,
        'candidate_in_contest':cd.CANDIDATE_IN_CONTEST_IMPORT,
        },
        'key_sources':{
            #'precinct':1,
            #'district':1,
            #'locality':1,
            },
        'parallel_load':(
            {'tables':('precinct','locality','legislative_district','congressional_district','judicial_district','school_district','county_council','county','state','legislative_district__precinct','congressional_district__precinct','judicial_district__precinct','school_district__precinct','county_council__precinct','county__precinct','state__precinct'),'keys':{}},
            )
        })
