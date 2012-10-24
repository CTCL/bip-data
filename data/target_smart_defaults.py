from data import univ_settings
from data import state_specific as ss
ss = reload(ss)
from data import table_defaults as td
td = reload(td)
import os
VFMAX=34
VIP_TABLES = {
        'election_administration':None,
        'election_official':None,
        'election':None,
        'locality':None,
        'polling_location':None,
        'precinct_polling_location':None,
        'precinct':None,
        'source':None,
        'state':None,
        'street_segment':None,
        'electoral_district':None, #'full',part_cat','part_col','part_cat_col',
        'candidiate':None #'full',part_cat','part_col','part_cat_col',
        }

PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
PRECINCT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
PRECINCT_IMPORT['udcs'].update({'is_split':False})
PRECINCT_IMPORT.update({
    'table':'precinct_import',
    'columns':{
        'name':29,
        'number':28,
        'ward':27,
        'locality_id_long':22,
        'identifier':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        'id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #        'locality_id':{'key':'locality'},
        #'id':{'key':'precinct'},
        }
    })

PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
PRECINCT_ACTUAL.update({
    'schema_table':'precinct',
    'import_table':PRECINCT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'locality_id_long','real':'locality_id'}),
    'distinct_on':('id_long',),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'locality_import',
            'local_key':'locality_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
        },
        )
    })

LOCALITY_IMPORT = dict(td.DEFAULT_VF_TABLE)
LOCALITY_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
LOCALITY_IMPORT['udcs'].update({'type':'COUNTY'})
LOCALITY_IMPORT.update({
    'table':'locality_import',
    'columns':{
        #        'id':{'key':'locality'},
        'name':22,
        'id_long':22,
        }
    })

LOCALITY_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
LOCALITY_ACTUAL.update({
    'schema_table':'locality',
    'import_table':LOCALITY_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'distinct_on':('id_long',),
    'long_from':('id_long',),
    })

CONGRESSIONAL_DISTRICT_IMPORT = dict(td.DEFAULT_VF_TABLE)
CONGRESSIONAL_DISTRICT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
CONGRESSIONAL_DISTRICT_IMPORT['udcs'].update({'type':'congressional_district'})
CONGRESSIONAL_DISTRICT_IMPORT.update({
    'table':'electoral_district_cd_import',
    'columns':{
        #'id':{'key':'congressional_district'},
        'name':23,
        'identifier':{'function':td.reformat.ed_concat,'columns':(23,),'defaults':{'type':'congressional_district'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(23,),'defaults':{'type':'congressional_district'}}
        },
    })

CONGRESSIONAL_DISTRICT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
CONGRESSIONAL_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':CONGRESSIONAL_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

JUDICIAL_DISTRICT_IMPORT = dict(td.DEFAULT_VF_TABLE)
JUDICIAL_DISTRICT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
JUDICIAL_DISTRICT_IMPORT['udcs'].update({'type':'judicial_district'})
JUDICIAL_DISTRICT_IMPORT.update({
    'table':'electoral_district_jd_import',
    'columns':{
        #'id':{'key':'judicial_district'},
        'name':34,
        'identifier':{'function':td.reformat.ed_concat,'columns':(34,),'defaults':{'type':'judicial_district'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(34,),'defaults':{'type':'judicial_district'}}
        },
    })

JUDICIAL_DISTRICT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
JUDICIAL_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':JUDICIAL_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

SCHOOL_DISTRICT_IMPORT = dict(td.DEFAULT_VF_TABLE)
SCHOOL_DISTRICT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
SCHOOL_DISTRICT_IMPORT['udcs'].update({'type':'school_district'})
SCHOOL_DISTRICT_IMPORT.update({
    'table':'electoral_district_schd_import',
    'columns':{
        'name':33,
        'identifier':{'function':td.reformat.ed_concat,'columns':(33,),'defaults':{'type':'school_district'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(33,),'defaults':{'type':'school_district'}}
        },
    })

SCHOOL_DISTRICT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
SCHOOL_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':SCHOOL_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

STATE_REP_DISTRICT_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE_REP_DISTRICT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
STATE_REP_DISTRICT_IMPORT['udcs'].update({'type':'state_rep_district'})
STATE_REP_DISTRICT_IMPORT.update({
    'table':'electoral_district_srd_import',
    'columns':{
        #'id':{'key':'state_rep_district'},
        'name':25,
        'identifier':{'function':td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'state_rep_district'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'state_rep_district'}}
        },
    })

STATE_REP_DISTRICT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE_REP_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':STATE_REP_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

STATE_SENATE_DISTRICT_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE_SENATE_DISTRICT_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
STATE_SENATE_DISTRICT_IMPORT['udcs'].update({'type':'state_senate_district'})
STATE_SENATE_DISTRICT_IMPORT.update({
    'table':'electoral_district_ssd_import',
    'columns':{
        #'id':{'key':'state_senate_district'},
        'name':24,
        'identifier':{'function':td.reformat.ed_concat,'columns':(24,),'defaults':{'type':'state_senate_district'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(24,),'defaults':{'type':'state_senate_district'}}
        },
    })

STATE_SENATE_DISTRICT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE_SENATE_DISTRICT_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':STATE_SENATE_DISTRICT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

COUNTY_COUNCIL_IMPORT = dict(td.DEFAULT_VF_TABLE)
COUNTY_COUNCIL_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
COUNTY_COUNCIL_IMPORT['udcs'].update({'type':'county_council'})
COUNTY_COUNCIL_IMPORT.update({
    'table':'electoral_district_cc_import',
    'columns':{
        #'id':{'key':'county_council'},
        'name':{'function':td.reformat.concat_us, 'columns':(22,30,)},
        'identifier':{'function':td.reformat.ed_concat,'columns':(22,30,),'defaults':{'type':'county_council'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(22,30,),'defaults':{'type':'county_council'}}
        },
    })

COUNTY_COUNCIL_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
COUNTY_COUNCIL_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':COUNTY_COUNCIL_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

COUNTY_IMPORT = dict(td.DEFAULT_VF_TABLE)
COUNTY_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
COUNTY_IMPORT['udcs'].update({'type':'county'})
COUNTY_IMPORT.update({
    'table':'electoral_district_c_import',
    'columns':{
        #'id':{'key':'county_council'},
        'name':22,
        'identifier':{'function':td.reformat.ed_concat,'columns':(22,),'defaults':{'type':'county'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(22,),'defaults':{'type':'county'}}
        },
    })

COUNTY_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
COUNTY_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':COUNTY_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

STATE_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE_IMPORT['udcs'] = dict(td.DEFAULT_VF_TABLE['udcs'])
STATE_IMPORT['udcs'].update({'type':'state'})
STATE_IMPORT.update({
    'table':'electoral_district_s_import',
    'columns':{
        #'id':{'key':'county_council'},
        'name':20,
        'identifier':{'function':td.reformat.ed_concat,'columns':(20,),'defaults':{'type':'state'}},
        'id_long':{'function':td.reformat.ed_concat,'columns':(20,),'defaults':{'type':'state'}}
        },
    })

STATE_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE_ACTUAL.update({
    'schema_table':'electoral_district',
    'import_table':STATE_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    'distinct_on':('id_long',),
    })

CONGRESSIONAL_DISTRICT__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
CONGRESSIONAL_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_cd_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'congressional_district'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(23,),'defaults':{'type':'congressional_district'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

CONGRESSIONAL_DISTRICT__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
CONGRESSIONAL_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':CONGRESSIONAL_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_cd_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

JUDICIAL_DISTRICT__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
JUDICIAL_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_jd_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #        'electoral_district_id':{'key':'judicial_district'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(34,),'defaults':{'type':'judicial_district'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

JUDICIAL_DISTRICT__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
JUDICIAL_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':JUDICIAL_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_jd_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

SCHOOL_DISTRICT__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
SCHOOL_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_schd_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(33,),'defaults':{'type':'school_district'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        },
    })

SCHOOL_DISTRICT__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
SCHOOL_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':SCHOOL_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_schd_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

STATE_REP_DISTRICT__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE_REP_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_srd_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'state_rep_district'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(25,),'defaults':{'type':'state_rep_district'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

STATE_REP_DISTRICT__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE_REP_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':STATE_REP_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_srd_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

STATE_SENATE_DISTRICT__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE_SENATE_DISTRICT__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_ssd_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'state_senate_district'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(24,),'defaults':{'type':'state_senate_district'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

STATE_SENATE_DISTRICT__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE_SENATE_DISTRICT__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':STATE_SENATE_DISTRICT__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_ssd_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

COUNTY_COUNCIL__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
COUNTY_COUNCIL__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_cc_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'county_council'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(22,30,),'defaults':{'type':'county_council'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

COUNTY_COUNCIL__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
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

COUNTY__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
COUNTY__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_c_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'county_council'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(22,),'defaults':{'type':'county'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

COUNTY__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
COUNTY__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':COUNTY__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_c_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

STATE__PRECINCT_IMPORT = dict(td.DEFAULT_VF_TABLE)
STATE__PRECINCT_IMPORT.update({
    'table':'electoral_district__precinct_s_import',
    'filename':ss.VOTER_FILE_LOCATION,
    'columns':{
        #'electoral_district_id':{'key':'county_council'},
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(20,),'defaults':{'type':'state'}},
        'precinct_id_long':{'function':td.reformat.concat_us,'columns':(22,29,28)},
        #'precinct_id':{'key':'precinct'},
        },
    })

STATE__PRECINCT_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
STATE__PRECINCT_ACTUAL.update({
    'schema_table':'electoral_district__precinct',
    'import_table':STATE__PRECINCT_IMPORT,
    'long_fields':({'long':'electoral_district_id_long','real':'electoral_district_id'},{'long':'precinct_id_long','real':'precinct_id'},),
    'distinct_on':('precinct_id_long','electoral_district_id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_s_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

ELECTORAL_DISTRICT_UNION = {
        'name':'electoral_district_import',
        'components':(
            'electoral_district_cd_import',
            'electoral_district_jd_import',
            'electoral_district_schd_import',
            'electoral_district_srd_import',
            'electoral_district_ssd_import',
            'electoral_district_cc_import',
            'electoral_district_c_import',
            'electoral_district_s_import',
            )
        }
"""
VOTER_FILE = dict(td.DEFAULT_TABLE)
VOTER_FILE.update({
        'table':'voter_file',
        'filename':ss.VOTER_FILE_LOCATION,
        'field_sep':'\t',
        'udcs':{
            'source':ss.VF_SOURCE,
            'election_key':ss.ELECTION,
            'residential_country':'USA',
            'mailing_country':'USA'
            },
        'columns':{
            'sos_voterid':1,
            'county_number':21,
            'county_id':22,
            ('residential_address1', 'residential_secondary_addr'):{'function':td.reformat.create_vf_address,'columns':(80,81,82,83,84,85,86)},
            'residential_city':76,
            'residential_state':77,
            'residential_zip':78,
            'residential_zip_plus4':79,
            #'residential_postalcode':18,
            ('mailing_address1', 'mailing_secondary_address'):{'function':td.reformat.create_vf_address,'columns':(96,97,98,99,100,101,102)},
            'mailing_city':92,
            'mailing_state':93,
            'mailing_zip':94,
            'mailing_zip_plus4':95,
            #'mailing_postal_code':26,
            'state':20,
            'county_council':30,
            'city_council':31,
            'municipal_district':32,
            'school_district':33,
            'judicial_district':34,
            'congressional_district':23,
            'precinct_name':29,
            'precinct_code':28,
            'state_rep_district':25,
            'state_senate_district':24,
            'township':26,
            #'village':44,
            'ward':27
            },
        'force_not_null':('sos_voterid','county_number'),
        })

ERSATZPG_CONFIG.update({
    'tables':{
        #'voter_file':VOTER_FILE,
        'precinct':PRECINCT,
        'locality':LOCALITY,
        'congressional_district':CONGRESSIONAL_DISTRICT,
        'state_rep_district':STATE_REP_DISTRICT,
        'judicial_district':JUDICIAL_DISTRICT,
        'county_council':COUNTY_COUNCIL,
        'state_senate_district':STATE_SENATE_DISTRICT,
        'congressional_district__precinct':CONGRESSIONAL_DISTRICT__PRECINCT,
        'state_rep_district__precinct':STATE_REP_DISTRICT__PRECINCT,
        'state_senate_district__precinct':STATE_SENATE_DISTRICT__PRECINCT,
        'judicial_district__precinct':JUDICIAL_DISTRICT__PRECINCT,
        'county_council__precinct':COUNTY_COUNCIL__PRECINCT,
        'candidate':CANDIDATE_LONG,
        'contest':CONTEST_LONG,
        'candidate_in_contest':CANDIDATE_IN_CONTEST_LONG
        },
        'key_sources':{
            'precinct':1,
            'district':1,
            'locality':1,
            },
        'parallel_load':(
            {'tables':('precinct','congressional_district', 'congressional_district__precinct','state_rep_district','state_rep_district__precinct','state_senate_district','state_senate_district__precinct','judicial_district','judicial_district__precinct','county_council','county_council__precinct','locality'),'keys':{'precinct':'precinct','congressional_district':'district','state_rep_district':'district','state_senate_district':'district','judicial_district':'district','county_council':'district','locality':'locality'}},)
            })
"""

VOTER_FILE_DISTRICTS = (
'state',
'county_id',
'county_council',
#'city_council',
#'municipal_district',
'school_district',
'judicial_district',
'congressional_district',
'state_rep_district',
'state_senate_district',
#'township',
#'ward'
)


TABLE_GROUP = {
        'default':td.DEFAULT_VF_TABLE,
        'tables':
        (
        PRECINCT_ACTUAL,
        LOCALITY_ACTUAL,
        CONGRESSIONAL_DISTRICT_ACTUAL,
        STATE_REP_DISTRICT_ACTUAL,
        JUDICIAL_DISTRICT_ACTUAL,
        SCHOOL_DISTRICT_ACTUAL,
        COUNTY_COUNCIL_ACTUAL,
        COUNTY_ACTUAL,
        STATE_SENATE_DISTRICT_ACTUAL,
        CONGRESSIONAL_DISTRICT__PRECINCT_ACTUAL,
        STATE_REP_DISTRICT__PRECINCT_ACTUAL,
        JUDICIAL_DISTRICT__PRECINCT_ACTUAL,
        SCHOOL_DISTRICT__PRECINCT_ACTUAL,
        COUNTY_COUNCIL__PRECINCT_ACTUAL,
        COUNTY__PRECINCT_ACTUAL,
        STATE_SENATE_DISTRICT__PRECINCT_ACTUAL,
        )
        }

#ELECTION_ADMINISTRATION_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'election_administration.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#ELECTION_OFFICIAL_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'election_official.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#ELECTION_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'election.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#POLLING_LOCATION_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'polling_location.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#PRECINCT_POLLING_LOCATION_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'precinct_polling_location.txt')})
#PRECINCT_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'precinct.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#SOURCE_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'source.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#STATE_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'state.txt'), 'udcs':{'source':VIP_SOURCE}})
#STREET_SEGMENT_LONG.update({'filename':os.path.join(VIP_FEED_LOCATION,'street_segment.txt'), 'udcs':{'source':VIP_SOURCE,'election_key':univ_settings.ELECTION}})
#GEO_ADDRESS_LONG_POLLING_LOCATION.update({'filename':os.path.join(VIP_FEED_LOCATION,'polling_location.txt')})
#GEO_ADDRESS_LONG_STREET_SEGMENT.update({'filename':os.path.join(VIP_FEED_LOCATION,'street_segment.txt')})
#GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS.update({'filename':os.path.join(VIP_FEED_LOCATION,'election_administration.txt')})
#GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_MAILING_ADDRESS.update({'filename':os.path.join(VIP_FEED_LOCATION,'election_administration.txt')})
