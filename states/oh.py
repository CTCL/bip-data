from states.base import StateBase
from deploy.conf import settings

#geo_county 
#	id
#	electoral_district_id
#electoral_district 
#	id
#	name
#	type
#	number
#geo_cd 
#	id
#	electoral_district_id
#referendum 
#	id
#	title
#	subtitle
#	brief
#	text
#	pro_statement
#	con_statement
#	contest_id
#	passage_threshold
#	effect_of_abstain
#polling_location 
#	id
#	address
#	directions
#	polling_hours
#	photo_url
#election 
#	id
#	date
#	election_type
#	state_id
#	statewide
#	registration_info
#	absentee_ballot_info
#	results_url
#	polling_hours
#	election_day_registration
#	registration_deadline
#	absentee_request_deadline
#candidate_in_contest 
#	sort_order
#	contest_id
#	candidate_id
#geo_address 
#	id
#	is_standardized
#	is_geocoded
#	house_number
#	house_number_prefix
#	hosue_number_suffix
#	street_direction
#	location_name
#	line3
#	line2
#	line1
#	city
#	state
#	zip4
#	zip
#	xcoord
#	ycoord
#	apartment
#candidate 
#	id
#	name
#	party
#	candidate_url
#	biography
#	phone
#	photo_url
#	filed_mailing_address
#	email
#	incumbent
#	google_plus_url
#	twitter_name
#	facebook_url
#	wiki_word
#contest 
#	id
#	election_id
#	electoral_district_id
#	partisan
#	type
#	primary_party
#	electorate_specifications
#	special
#	office
#	filing_closed_date
#	number_elected
#	number_voting_for
#	ballot_placement
#	contest_type
#	write_in
#	custom_ballot_heading
#election_administration 
#	id
#	name
#	ovc_id
#	eo_id
#	physical_address
#	mailing_address
#	elections_url
#	type
#	state_id
#	hours
#	voter_services
#	rules_url
#	what_is_on_my_ballot_url
#	where_do_i_vote_url
#	absentee_url
#	am_i_registered_url
#	registration_url
#source 
#	id
#	user_id
#	source_data_file_url
#	hash
#	aquired
#	reviewed
#	reviewing_user_id
#state 
#	id
#	name
#	postal_code
#early_vote_site 
#	id
#	name
#	address
#	directions
#	voter_services
#	start_date
#	end_date
#	state_id
#	days_time_open
#precinct__polling_location 
#	precinct_id
#	polling_location_id
#precinct 
#	id
#	name
#	number
#	electoral_district
#	ward
#	mail_only
#	polling_location_id
#	early_vote_site_id
#	ballot_style_image_url
#	election_administration_id
#	state_id
#electoral_district__precinct 
#	electoral_district_id
#	precinct_id
#precinct__early_vote_site 
#	precinct_id
#	early_vote_site_id
#geo_ss 
#	id
#	electoral_district_id
#ballot_response 
#	id
#	contest_id
#	sort_order
#	text
#geo_sh 
#	id
#	electoral_district_id
#election_official 
#	id
#	title
#	phone
#	fax
#	email
#	name
#org_custom_field 
#	parent_id
#	key
#	value
#	type
#	org_id


from pipeline.feedripper import do_viacsv

class State(StateBase):
	ripper = do_viacsv()
	def _get_feed_path(self):
		return 'data/vip_feeds/vipFeed-39-2012-03-06.xml'