from data import state_specific as ss
ss = reload(ss)
from data import table_defaults as td
td = reload(td)

CONTEST_IMPORT = dict(td.DEFAULT_CANDIDATE_TABLE)
CONTEST_IMPORT['udcs'] = dict(td.DEFAULT_CANDIDATE_TABLE['udcs']) 
CONTEST_IMPORT['udcs'].update({'contest_type':'candidate'}) 
CONTEST_IMPORT.update({ 
    'sources':td.CANDIDATE_SOURCE_POSSIBLES + td.REFERENDUM_SOURCE_POSSIBLES,
    'table':'contest_import',
    'columns':{
        'identifier':{'function':td.reformat.contest_id,'columns':(2,4,5)},
        'id_long':{'function':td.reformat.contest_id,'columns':(2,4,5)},
        'office_level':3,
        'state':2,
        'office':5,
        ('electoral_district_name', 'electoral_district_type','electoral_district_id_long','ed_matched'):{'function': ss.STATE_EDMAP, 'columns':(4,)},
        }
    })

CONTEST_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
CONTEST_ACTUAL.update({
    'schema_table':'contest',
    'import_table':CONTEST_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'electoral_district_id_long','real':'electoral_district_id'}),
    'distinct_on':('id_long',),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

BALLOT_CONTEST_IMPORT = dict(td.DEFAULT_CANDIDATE_TABLE)
BALLOT_CONTEST_IMPORT['udcs'] = dict(td.DEFAULT_CANDIDATE_TABLE['udcs'])
BALLOT_CONTEST_IMPORT['udcs'].update({'contest_type':'referendum','electoral_district_type':'state','office':'statewide referendum','office_level':'Statewide','source':'referenda'})
BALLOT_CONTEST_IMPORT.update({
    'sources':td.CANDIDATE_SOURCE_POSSIBLES + td.REFERENDUM_SOURCE_POSSIBLES,
    'filename':ss.REFERENDUM_FILE_LOCATION,
    'table':'contest_import',
    'columns':{
        'identifier':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'id_long':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'state':2,
        'electoral_district_name':2,
        'electoral_district_id_long':{'function':td.reformat.ed_concat,'columns':(2,),'defaults':{'type':'state'}},
        }
    })

BALLOT_CONTEST_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
BALLOT_CONTEST_ACTUAL.update({
    'schema_table':'contest',
    'import_table':BALLOT_CONTEST_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'electoral_district_id_long','real':'electoral_district_id'}),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'electoral_district_import',
            'local_key':'electoral_district_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

REFERENDUM_IMPORT = dict(td.DEFAULT_REFERENDUM_TABLE)
REFERENDUM_IMPORT.update({
    'table':'referendum_import',
    'columns':{
        'identifier':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'id_long':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'contest_id_long':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'title':3,
        'subtitle':4,
        'brief':5,
        'text':6,
        }
    })

REFERENDUM_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
REFERENDUM_ACTUAL.update({
    'schema_table':'referendum',
    'import_table':REFERENDUM_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'contest_id_long','real':'contest_id'}),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'contest_import',
            'local_key':'contest_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

BALLOT_RESPONSE_ONE_IMPORT = dict(td.DEFAULT_REFERENDUM_TABLE)
BALLOT_RESPONSE_ONE_IMPORT.update({
    'table':'ballot_response_one_import',
    'columns':{
        'referendum_id_long':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'text':7,
        }
    })

BALLOT_RESPONSE_ONE_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
BALLOT_RESPONSE_ONE_ACTUAL.update({
    'schema_table':'ballot_response',
    'import_table':BALLOT_RESPONSE_ONE_IMPORT,
    'long_fields':({'long':'referendum_id_long','real':'referendum_id'},),
    'long_to':(
        {
            'to_table':'referendum_import',
            'local_key':'referendum_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

BALLOT_RESPONSE_TWO_IMPORT = dict(td.DEFAULT_REFERENDUM_TABLE)
BALLOT_RESPONSE_TWO_IMPORT.update({
    'table':'ballot_response_two_import',
    'columns':{
        'referendum_id_long':{'function':td.reformat.referendum_id,'columns':(2,3)},
        'text':8,
        }
    })

BALLOT_RESPONSE_TWO_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
BALLOT_RESPONSE_TWO_ACTUAL.update({
    'schema_table':'ballot_response',
    'import_table':BALLOT_RESPONSE_TWO_IMPORT,
    'long_fields':({'long':'referendum_id_long','real':'referendum_id'},),
    'long_to':(
        {
            'to_table':'referendum_import',
            'local_key':'referendum_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

BALLOT_RESPONSE_UNION = {
        'name':'ballot_response_import',
        'components':(
            'ballot_response_one_import',
            'ballot_response_two_import',
            )
        }

CANDIDATE_IN_CONTEST_IMPORT = dict(td.DEFAULT_CANDIDATE_TABLE)
CANDIDATE_IN_CONTEST_IMPORT.update({
    'table':'candidate_in_contest_import',
    'columns':{
        'candidate_id_long':1,
        'contest_id_long':{'function':td.reformat.contest_id,'columns':(2,4,5)},
        },
    })

CANDIDATE_IN_CONTEST_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
CANDIDATE_IN_CONTEST_ACTUAL.update({
    'schema_table':'candidate_in_contest',
    'import_table':CANDIDATE_IN_CONTEST_IMPORT,
    'long_fields':({'long':'candidate_id_long','real':'candidate_id'},{'long':'contest_id_long','real':'contest_id'}),
    'long_to':(
        {
            'to_table':'candidate_import',
            'local_key':'candidate_id_long',
            'to_key':'id_long',
            'real_to_key':'id'
            },
        {
            'to_table':'contest_import',
            'local_key':'contest_id_long',
            'to_key':'id_long',
            'real_to_key':'id'
            }
        )
    })

CANDIDATE_IMPORT = dict(td.DEFAULT_CANDIDATE_TABLE)
CANDIDATE_IMPORT.update({
    'table':'candidate_import',
    'columns':{
        'id_long':1,
        'identifier':1,
        #'office_level':3,
        #'office_name':5,
        'name':6,
        'party':7,
        'incumbent':9,
        'phone':10,
        'mailing_address':11,
        'candidate_url':12,
        'email':13,
        'facebook_url':14,
        'twitter_name':15,
        'google_plus_url':16,
        'wiki_word':17,
        'youtube':18
        },
    })

CANDIDATE_ACTUAL = dict(td.DEFAULT_ACTUAL_TABLE)
CANDIDATE_ACTUAL.update({
    'schema_table':'candidate',
    'import_table':CANDIDATE_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })

