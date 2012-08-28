from state_abbr import states
from data import univ_settings
reformat = univ_settings.table_functions
from data.state_specific import *
VIP_SOURCE_POSSIBLES = [s+'VIP' for s in states]
VF_SOURCE_POSSIBLES = [s+'VF' for s in states]
CANDIDATE_SOURCE_POSSIBLES = [s+'Candidates' for s in states]
ELECTION_POSSIBLES = ['2012']
DEFAULT_TABLE = {
        'skip_head_lines':1,
        'format':'csv',
        'field_sep':',',
        'quotechar':'"',
        'copy_every':100000,
        'udcs':{
            'election_key':ELECTION,
            'source':VIP_SOURCE
            },
        'sources':VIP_SOURCE_POSSIBLES,
        'elections':ELECTION_POSSIBLES,
        }

DEFAULT_VF_TABLE = dict(DEFAULT_TABLE)
DEFAULT_VF_TABLE.update({
    'filename':VOTER_FILE_LOCATION,
    'field_sep':'\t',
    'udcs':{
        'source':VF_SOURCE,
        'election_key':ELECTION,
        },
        'sources':VF_SOURCE_POSSIBLES,
    })

DEFAULT_CANDIDATE_TABLE = dict(DEFAULT_TABLE)
DEFAULT_CANDIDATE_TABLE.update({
    'filename':CANDIDATE_FILE_LOCATION,
    'udcs':{
        'source':CANDIDATE_SOURCE,
        'election_key':ELECTION,
        },
        'sources':CANDIDATE_SOURCE_POSSIBLES,
    })

DEFAULT_ACTUAL_TABLE = {
        'long_fields':(),
        'long_from':(),
        'long_to':(),
        }
