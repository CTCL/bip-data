from data import univ_settings
reformat = univ_settings.table_functions
DEFAULT_TABLE = {
        'skip_head_lines':1,
        'format':'csv',
        'field_sep':',',
        'quotechar':'"',
        'copy_every':500000
        }

ELECTION_ADMINISTRATION_LONG = dict(DEFAULT_TABLE)
ELECTION_ADMINISTRATION_LONG.update({
        'table':'election_administration_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'name':1,
            'eo_id_long':2,
            'ovc_id_long':3,
            'elections_url':18,
            'registration_url':19,
            'am_i_registered_url':20,
            'absentee_url':21,
            'where_do_i_vote_url':22,
            'what_is_on_my_ballot_url':23,
            'rules_url':24,
            'voter_services':25,
            'hours':26,
            'id_long':27,
            'mailing_address_long':{'function':reformat.address_seq,'columns':()},
            'physical_address_long':{'function':reformat.address_seq,'columns':()},
            }
        })
GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS = dict(DEFAULT_TABLE)
GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS.update({
        'table':'geo_address_long',
        'columns':{
            'location_name':9,
            'line1':8,
            'line2':7,
            'line3':6,
            'city':5,
            'state':4,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(10,)},
            'id_long':{'function':reformat.address_seq,'columns':()},
            }
        })

GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_MAILING_ADDRESS = dict(DEFAULT_TABLE)
GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_MAILING_ADDRESS.update({
        'table':'geo_address_long',
        'columns':{
            'location_name':15,
            'line1':12,
            'line2':13,
            'line3':14,
            'city':17,
            'state':11,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(16,)},
            'id_long':{'function':reformat.address_seq,'columns':()},
            }
        })

ELECTION_LONG = dict(DEFAULT_TABLE)
ELECTION_LONG.update({
        'table':'election_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'date':1,
            'election_type':2,
            'state_id_long':3,
            'statewide':4,
            'registration_info':5,
            'absentee_ballot_info':6,
            'results_url':7,
            'polling_hours':8,
            'election_day_registration':9,
            'registration_deadline':10,
            'absentee_request_deadline':11,
            'id_long':12
            }
        })

POLLING_LOCATION_LONG = dict(DEFAULT_TABLE)
POLLING_LOCATION_LONG.update({
        'table':'polling_location_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'directions':8,
            'polling_hours':9,
            'photo_url':10,
            'id_long':11,
            'address_long':{'function':reformat.address_seq,'columns':()},
            }
        })

GEO_ADDRESS_LONG_POLLING_LOCATION = dict(DEFAULT_TABLE)
GEO_ADDRESS_LONG_POLLING_LOCATION.update({
        'table':'geo_address_long',
        'columns':{
            'location_name':6,
            'line1':4,
            'line2':1,
            'line3':2,
            'city':3,
            'state':5,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(7,)},
            'id_long':{'function':reformat.address_seq,'columns':()},
            }
        })

SOURCE_LONG = dict(DEFAULT_TABLE)
SOURCE_LONG.update({
        'table':'source_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'name':1,
            'vip_id':2,
#            'id_long':8,
#            'acquired':
            'description':4,
            'organization_url':5
            }
        })

PRECINCT_LONG = dict(DEFAULT_TABLE)
PRECINCT_LONG.update({
        'table':'precinct_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'name':1,
            'number':2,
            'locality_id':3,
            #'electoral_district_id':4,
            'ward':4,
            'mail_only':5,
            #'polling_location_id_long':7,
            #'early_vote_site_id':8,
            'ballot_style_image_url':6,
            'id_long':7
            }
        })

STREET_SEGMENT_LONG = dict(DEFAULT_TABLE)
STREET_SEGMENT_LONG.update({
        'table':'street_segment_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'start_house_number':1,
            'end_house_number':2,
            'odd_even_both':3,
            'start_apartment_number':4,
            'end_apartment_number':5,
            'precinct_id_long':17,
            'precinct_split_id_long':18,
            'id':19,
            'non_house_address_long':{'function':reformat.address_seq,'columns':()},
            }
        })

GEO_ADDRESS_LONG_STREET_SEGMENT = dict(DEFAULT_TABLE)
GEO_ADDRESS_LONG_STREET_SEGMENT.update({
        'table':'geo_address_long',
        'columns':{
            'house_number':16,
            'house_number_prefix':8,
            'house_number_suffix':13,
            'street_direction':12,
            'street_name':7,
            'street_suffix':10,
            'address_direction':6,
            'apartment':15,
            'city':9,
            'state':11,
            'zip':14,
            'id_long':{'function':reformat.address_seq,'columns':()},
            }
        })

ELECTION_OFFICIAL_LONG = dict(DEFAULT_TABLE)
ELECTION_OFFICIAL_LONG.update({
        'table':'election_official_long',
        'udcs':{
            'election_key':univ_settings.ELECTION
            },
        'columns':{
            'name':1,
            'title':2,
            'phone':3,
            'fax':4,
            'email':5,
            'id_long':6
            }
        })
"""
LOCALITY_LONG = dict(DEFAULT_TABLE)
LOCALITY_LONG.update({
        'table':'locality_long',
        'columns':{
            'name':1,
            'state_id_long':2,
            'type':3,
            'election_administration_id_long':4,
            'id_long':5
            }
        })
"""
PRECINCT_POLLING_LOCATION_LONG = dict(DEFAULT_TABLE)
PRECINCT_POLLING_LOCATION_LONG.update({
        'table':'precinct__polling_location_long',
        'columns':{
            'precinct_id_long':1,
            'polling_location_id_long':2
            }
        })

STATE_LONG = dict(DEFAULT_TABLE)
STATE_LONG.update({
        'table':'state_long',
        'columns':{
            'name':1,
            #'election_administration_id_long':2,
            'id_long':3
            }
        })

ERSATZPG_CONFIG = univ_settings.ERSATZPG_CONFIG
ERSATZPG_CONFIG.update({
        'tables':{
            'election_administration':ELECTION_ADMINISTRATION_LONG,
            'election_official':ELECTION_OFFICIAL_LONG,
            'election':ELECTION_LONG,
            'polling_location':POLLING_LOCATION_LONG,
            'precinct__polling_location':PRECINCT_POLLING_LOCATION_LONG,
            'precinct':PRECINCT_LONG,
            'source':SOURCE_LONG,
            'state':STATE_LONG,
            'street_segment':STREET_SEGMENT_LONG,
            'geo_address_long_polling_location':GEO_ADDRESS_LONG_POLLING_LOCATION,
            'geo_address_long_street_segment':GEO_ADDRESS_LONG_STREET_SEGMENT,
            'geo_address_long_election_administration_physical_address':GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS,
            'geo_address_long_election_administration_mailing_address':GEO_ADDRESS_LONG_ELECTION_ADMINISTRATION_MAILING_ADDRESS,
            },
        'parallel_load':(
            {'tables':('polling_location','geo_address_long_polling_location'), 'keys':{'address':'geo_address',}},
            {'tables':('street_segment','geo_address_long_street_segment'), 'keys':{'non_house_address':'geo_address',}},
            {'tables':('election_administration','geo_address_long_election_administration_physical_address','geo_address_long_election_administration_mailing_address'), 'keys':{'physical_address':'geo_address','mailing_address':'geo_address'}},
            ),
        'key_sources':{
            'geo_address':1
            }
        })
