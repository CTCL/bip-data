from data.state_specific import *
from data.table_defaults import *
import os

ELECTION_ADMINISTRATION_IMPORT = dict(DEFAULT_TABLE)
ELECTION_ADMINISTRATION_IMPORT.update({
        'table':'election_administration_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'election_administration.txt'])
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
            'mailing_address':{'key':'mailing_address'},
            'physical_address':{'key':'physical_address'},
            }
        })

ELECTION_ADMINISTRATION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
ELECTION_ADMINISTRATION_ACTUAL.update({
    'schema_table':'election_administration',
    'import_table':ELECTION_ADMINISTRATION_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'eo_id_long','real':'eo_id'},{'long':'ovc_id_long','real':'ovc_id'}),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'election_official_import',
            'local_key':'eo_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        {
            'to_table':'election_official',
            'local_key':'ovc_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

GEO_ADDRESS_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS_IMPORT = dict(DEFAULT_TABLE)
GEO_ADDRESS_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS_IMPORT.update({
        'table':'geo_address_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'election_administration.txt'])
        'columns':{
            'location_name':9,
            'line1':8,
            'line2':7,
            'line3':6,
            'city':5,
            'state':4,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(10,)},
            'id':{'key':'physical_address'},
            }
        })

GEO_ADDRESS_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
GEO_ADDRESS_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS_ACTUAL.update({
        'schema_table':'geo_address',
        'import_table':GEO_ADDRESS_ELECTION_ADMINISTRATION_PHYSICAL_ADDRESS_IMPORT,
        })

GEO_ADDRESS_ELECTION_ADMINISTRATION_MAILING_ADDRESS_IMPORT = dict(DEFAULT_TABLE)
GEO_ADDRESS_ELECTION_ADMINISTRATION_MAILING_ADDRESS_IMPORT.update({
        'table':'geo_address_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'election_administration.txt'])
        'columns':{
            'location_name':15,
            'line1':12,
            'line2':13,
            'line3':14,
            'city':17,
            'state':11,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(16,)},
            'id':{'key':'mailing_address'},
            }
        })

GEO_ADDRESS_ELECTION_ADMINISTRATION_MAILING_ADDRESS_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
GEO_ADDRESS_ELECTION_ADMINISTRATION_MAILING_ADDRESS_ACTUAL.update({
        'schema_table':'geo_address',
        'import_table':GEO_ADDRESS_ELECTION_ADMINISTRATION_MAILING_ADDRESS_IMPORT,
        })

ELECTION_IMPORT = dict(DEFAULT_TABLE)
ELECTION_IMPORT.update({
        'table':'election_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'election.txt'])
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

ELECTION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
ELECTION_ACTUAL.update({
    'schema_table':'election',
    'import_table':ELECTION_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'state_id_long','real':'state_id'},),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'state_import',
            'local_key':'state_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

POLLING_LOCATION_IMPORT = dict(DEFAULT_TABLE)
POLLING_LOCATION_IMPORT.update({
        'table':'polling_location_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'polling_location.txt'])
        'columns':{
            'directions':8,
            'polling_hours':9,
            'photo_url':10,
            'id_long':11,
            'address':{'key':'address'},
            }
        })

POLLING_LOCATION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
POLLING_LOCATION_ACTUAL.update({
    'schema_table':'polling_location',
    'import_table':POLLING_LOCATION_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })

GEO_ADDRESS_POLLING_LOCATION_IMPORT = dict(DEFAULT_TABLE)
GEO_ADDRESS_POLLING_LOCATION_IMPORT.update({
        'table':'geo_address_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'polling_location.txt'])
        'columns':{
            'location_name':6,
            'line1':4,
            'line2':1,
            'line3':2,
            'city':3,
            'state':5,
            ('zip','zip4'):{'function':reformat.zip_parse, 'columns':(7,)},
            'id':{'key':'address'},
            }
        })

GEO_ADDRESS_POLLING_LOCATION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
GEO_ADDRESS_POLLING_LOCATION_ACTUAL.update{
        'schema_table':'geo_address',
        'import_table':GEO_ADDRESS_POLLING_LOCATION_IMPORT,
        })

SOURCE_IMPORT = dict(DEFAULT_TABLE)
SOURCE_IMPORT.update({
        'table':'source_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'source.txt'])
        'columns':{
            'name':1,
            'vip_id':2,
#            'id_long':8,
#            'acquired':
            'description':4,
            'organization_url':5
            }
        })

SOURCE_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
SOURCE_ACTUAL.update{
        'schema_table':'source',
        'import_table':SOURCE_IMPORT,
        })

PRECINCT_IMPORT = dict(DEFAULT_TABLE)
PRECINCT_IMPORT.update({
        'table':'precinct_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'precinct.txt'])
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

PRECINCT_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
PRECINCT_ACTUAL.update({
    'schema_table':'precinct',
    'import_table':PRECINCT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })

STREET_SEGMENT_IMPORT = dict(DEFAULT_TABLE)
STREET_SEGMENT_IMPORT.update({
        'table':'street_segment_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'street_segment.txt'])
        'columns':{
            'start_house_number':1,
            'end_house_number':2,
            'odd_even_both':3,
            'start_apartment_number':4,
            'end_apartment_number':5,
            'precinct_id_long':17,
            'precinct_split_id_long':18,
            'id_long':19,
            'non_house_address':{'key':'non_house_address'},
            }
        })

STREET_SEGMENT_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
STREET_SEGMENT_ACTUAL.update({
    'schema_table':'street_segment',
    'import_table':STREET_SEGMENT_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},{'long':'precinct_id_long','real':'precinct_id'},{'long':'precinct_split_id_long','real':'precinct_split_id'},),
    'long_from':('id_long',),
    'long_to':(
        {
            'to_table':'precinct_import',
            'local_key':'precinct_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        {
            'to_table':'precinct',
            'local_key':'precinct_split_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

GEO_ADDRESS_STREET_SEGMENT_IMPORT = dict(DEFAULT_TABLE)
GEO_ADDRESS_STREET_SEGMENT_IMPORT.update({
        'table':'geo_address_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'street_segment.txt'])
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
            'id':{'key':'non_house_address'},
            }
        })

GEO_ADDRESS_STREET_SEGMENT_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
GEO_ADDRESS_STREET_SEGMENT_ACTUAL.update({
        'schema_table':'geo_address',
        'import_table':GEO_ADDRESS_STREET_SEGMENT_IMPORT,
        })

ELECTION_OFFICIAL_IMPORT = dict(DEFAULT_TABLE)
ELECTION_OFFICIAL_IMPORT.update({
        'table':'election_official_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'election_official.txt'])
        'columns':{
            'name':1,
            'title':2,
            'phone':3,
            'fax':4,
            'email':5,
            'id_long':6
            }
        })

ELECTION_OFFICIAL_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
ELECTION_OFFICIAL_ACTUAL.update({
    'schema_table':'election_official',
    'import_table':ELECTION_OFFICIAL_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })

"""
LOCALITY_IMPORT = dict(DEFAULT_TABLE)
LOCALITY_IMPORT.update({
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
PRECINCT__POLLING_LOCATION_IMPORT = dict(DEFAULT_TABLE)
PRECINCT__POLLING_LOCATION_IMPORT.update({
        'table':'precinct__polling_location_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'precinct__polling_location.txt'])
        'columns':{
            'precinct_id_long':1,
            'polling_location_id_long':2
            }
        })

PRECINCT__POLLING_LOCATION_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
PRECINCT__POLLING_LOCATION_ACTUAL.update({
    'schema_table':'precinct__polling_location',
    'import_table':PRECINCT__POLLING_LOCATION_IMPORT,
    'long_fields':({'long':'precinct_id_long','real':'precinct_id'},{'long':'polling_location_id_long','real':'polling_location_id'},),
    'long_to':(
        {
            'to_table':'precinct_import',
            'local_key':'precinct_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        {
            'to_table':'polling_location_import',
            'local_key':'polling_location_id_long',
            'to_key':'id_long',
            'real_to_key':'id',
            },
        ),
    })

STATE_IMPORT = dict(DEFAULT_TABLE)
STATE_IMPORT.update({
        'table':'state_import',
        'filename':os.path.join(*[VIP_FEED_LOCATION,'state.txt'])
        'columns':{
            'name':1,
            #'election_administration_id_long':2,
            'id_long':3
            }
        })

STATE_ACTUAL = dict(DEFAULT_ACTUAL_TABLE)
STATE_ACTUAL.update({
    'schema_table':'state',
    'import_table':STATE_IMPORT,
    'long_fields':({'long':'id_long','real':'id'},),
    'long_from':('id_long',),
    })

PARALLEL_LOAD = (
            {'tables':('polling_location','geo_address_polling_location'), 'keys':{'address':'geo_address',}},
            {'tables':('street_segment','geo_address_street_segment'), 'keys':{'non_house_address':'geo_address',}},
            {'tables':('election_administration','geo_address_election_administration_physical_address','geo_address_election_administration_mailing_address'), 'keys':{'physical_address':'geo_address','mailing_address':'geo_address'}},
            )

KEY_SOURCES = {
            'geo_address':1
            }
