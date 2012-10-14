from data import univ_settings
univ_settings = reload(univ_settings)
from data import state_specific
state_specific.VOTER_FILE_LOCATION = ''
state_specific.ELECTION = ''
state_specific.VIP_SOURCE = '' 
state_specific.VF_SOURCE = '' 
state_specific.CANDIDATE_SOURCE = '' 
state_specific.CANDIDATE_FILE_LOCATION = ''
state_specific.REFERENDUM_FILE_LOCATION = '' 
state_specific.STATE_EDMAP = lambda:''
from data import target_smart_defaults as tsd
tsd = reload(tsd)
from data import candidate_defaults as cd
cd = reload(cd)
ERSATZPG_CONFIG = univ_settings.ERSATZPG_CONFIG
ACTUAL_TABLES = (
        tsd.PRECINCT_ACTUAL,
        tsd.LOCALITY_ACTUAL,
        tsd.CONGRESSIONAL_DISTRICT_ACTUAL,
        tsd.STATE_REP_DISTRICT_ACTUAL,
        tsd.JUDICIAL_DISTRICT_ACTUAL,
        tsd.SCHOOL_DISTRICT_ACTUAL,
        tsd.COUNTY_COUNCIL_ACTUAL,
        tsd.COUNTY_ACTUAL,
        tsd.STATE_ACTUAL,
        tsd.STATE_SENATE_DISTRICT_ACTUAL,
        tsd.CONGRESSIONAL_DISTRICT__PRECINCT_ACTUAL,
        tsd.STATE_REP_DISTRICT__PRECINCT_ACTUAL,
        tsd.JUDICIAL_DISTRICT__PRECINCT_ACTUAL,
        tsd.SCHOOL_DISTRICT__PRECINCT_ACTUAL,
        tsd.COUNTY_COUNCIL__PRECINCT_ACTUAL,
        tsd.COUNTY__PRECINCT_ACTUAL,
        tsd.STATE_SENATE_DISTRICT__PRECINCT_ACTUAL,
        tsd.STATE__PRECINCT_ACTUAL,
        cd.CANDIDATE_ACTUAL,
        cd.CONTEST_ACTUAL,
        cd.CANDIDATE_IN_CONTEST_ACTUAL,
        cd.BALLOT_CONTEST_ACTUAL,
        cd.REFERENDUM_ACTUAL,
        cd.BALLOT_RESPONSE_ONE_ACTUAL,
        cd.BALLOT_RESPONSE_TWO_ACTUAL,
        )

UNIONS = (
        tsd.ELECTORAL_DISTRICT_UNION,
        cd.BALLOT_RESPONSE_UNION,
        )

VOTER_FILE = dict(tsd.td.DEFAULT_TABLE)
VOTER_FILE.update({
        'table':'voter_file',
        'filename':state_specific.VOTER_FILE_LOCATION,
        'field_sep':'\t',
        'udcs':{
            'source':state_specific.VF_SOURCE,
            'election_key':state_specific.ELECTION,
            'residential_country':'USA',
            'mailing_country':'USA'
            },
        'columns':{
            'sos_voterid':1,
            'county_number':21,
            'county_id':22,
            ('residential_address1', 'residential_secondary_addr'):{'function':tsd.td.reformat.create_vf_address,'columns':(80,81,82,83,84,85,86)},
            'residential_city':76,
            'residential_state':77,
            'residential_zip':78,
            'residential_zip_plus4':79,
            #'residential_postalcode':18,
            ('mailing_address1', 'mailing_secondary_address'):{'function':tsd.td.reformat.create_vf_address,'columns':(96,97,98,99,100,101,102)},
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
            'state_representative_district':25,
            'state_senate_district':24,
            'township':26,
            #'village':44,
            'ward':27
            },
        'force_not_null':('sos_voterid','county_number'),
        })
