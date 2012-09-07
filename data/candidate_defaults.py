from data import state_specific as ss
ss = reload(ss)
from data import table_defaults as td
td = reload(td)

CONTEST_IMPORT = dict(td.DEFAULT_CANDIDATE_TABLE)
CONTEST_IMPORT.update({
    'table':'contest_import',
    'columns':{
        'id_long':{'function':td.reformat.contest_id,'columns':(2,4,5)},
        'state':2,
        'office':5,
        ('electoral_district_name', 'electoral_district_type','electoral_district_id_long'):{'function': ss.STATE_EDMAP, 'columns':(4,)},
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

