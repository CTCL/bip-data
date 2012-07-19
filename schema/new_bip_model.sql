CREATE TYPE contestenum AS ENUM ('candidate','referendum','custom');
CREATE TYPE cfenum AS ENUM ('candidate','referendum ');
CREATE TYPE electionenum AS ENUM ('primary','general','state','Primary','General','State');
CREATE TYPE oddevenenum AS ENUM ('odd','even','both','BOTH','EVEN','ODD');
CREATE TYPE usstate AS ENUM ('AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MH', 'MA', 'MI', 'FM', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY');
CREATE SEQUENCE pksq START 1;
CREATE TABLE geo_county_long (
source text,
id int4 DEFAULT nextval('pksq'),
electoral_district_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE electoral_district_long (
name varchar(255),
state_id_long varchar(255),
number int4,
source text,
id_long varchar(255),
type varchar(255),
id int4 DEFAULT nextval('pksq'),
PRIMARY KEY (id)
);

CREATE TABLE geo_cd_long (
source text,
id int4 DEFAULT nextval('pksq'),
electoral_district_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE election_administration_long (
rules_url varchar(255),
ovc_id_long varchar(255),
id int4 DEFAULT nextval('pksq'),
am_i_registered_url varchar(255),
source text,
eo_id_long varchar(255),
type varchar(255),
physical_address_long varchar(255),
elections_url varchar(255),
absentee_url varchar(255),
state_id_long varchar(255),
hours varchar(255),
where_do_i_vote_url varchar(255),
voter_services varchar(255),
name varchar(255),
registration_url varchar(255),
id_long varchar(255),
what_is_on_my_ballot_url varchar(255),
mailing_address_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE polling_location_long (
source text,
polling_hours varchar(255),
address_long varchar(255),
id_long varchar(255),
directions varchar(255),
id int4 DEFAULT nextval('pksq'),
photo_url varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE election_long (
registration_deadline varchar(255),
id_long varchar(255),
statewide bool,
absentee_ballot_info varchar(255),
registration_info varchar(255),
election_type electionenum,
source text,
absentee_request_deadline varchar(255),
polling_hours varchar(255),
results_url varchar(255),
date date,
election_day_registration bool,
id int4 DEFAULT nextval('pksq'),
state_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE candidate_in_contest_long (
sort_order int4,
contest_id_long varchar(255),
candidate_id_long varchar(255),
PRIMARY KEY (contest_id_long,candidate_id_long)
);

CREATE TABLE geo_address_long (
street_name varchar(50),
line1 varchar(255),
house_number_prefix varchar(50),
id int4 DEFAULT nextval('pksq'),
zip4 varchar(4),
is_geocoded bool,
is_standardized bool,
apartment varchar(255),
location_name varchar(255),
ycoord varchar(255),
house_number int4,
line3 varchar(255),
line2 varchar(255),
street_suffix varchar(50),
source text,
state varchar(255),
city varchar(255),
xcoord varchar(255),
address_direction varchar(50),
house_number_suffix varchar(50),
zip varchar(10),
id_long varchar(255),
street_direction varchar(50),
PRIMARY KEY (id)
);

CREATE TABLE candidate_long (
filed_mailing_address_long varchar(255),
name varchar(255),
phone varchar(255),
facebook_url varchar(255),
email varchar(255),
candidate_url varchar(255),
source text,
google_plus_url varchar(255),
twitter_name varchar(255),
incumbent bool,
id_long varchar(255),
party varchar(255),
wiki_word varchar(255),
id int4 DEFAULT nextval('pksq'),
biography varchar(255),
photo_url varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE contest_long (
number_voting_for int4,
electoral_district_id_long varchar(255),
office varchar(255),
filing_closed_date date,
election_id_long varchar(255),
type varchar(255),
partisan bool,
number_elected int4,
custom_ballot_heading text,
contest_type contestenum,
electorate_specifications varchar(255),
write_in bool,
source text,
ballot_placement varchar(255),
id_long varchar(255),
primary_party varchar(255),
id int4 DEFAULT nextval('pksq'),
special bool,
PRIMARY KEY (id)
);

CREATE TABLE referendum_long (
subtitle varchar(255),
title varchar(255),
text varchar(255),
con_statement varchar(255),
effect_of_abstain varchar(255),
brief varchar(255),
source text,
contest_id_long varchar(255),
passage_threshold varchar(255),
id int4 DEFAULT nextval('pksq'),
pro_statement varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE source_long (
user_id int4,
name varchar(255),
acquired timestamp,
source_data_file_url varchar(255),
reviewing_user_id int4,
reviewed bool,
source text,
hash varchar(255),
organization_url varchar(255),
id int4 DEFAULT nextval('pksq'),
description text,
PRIMARY KEY (id)
);

CREATE TABLE state_long (
source text,
id_long varchar(255),
postal_code varchar(2),
id int4 DEFAULT nextval('pksq'),
name varchar(50),
PRIMARY KEY (id) ,
CONSTRAINT "unique_name" UNIQUE (name),
CONSTRAINT "unique_postal_code" UNIQUE (postal_code)
);

CREATE TABLE precinct__polling_location_long (
polling_location_id_long varchar(255),
precinct_id_long varchar(255),
PRIMARY KEY (precinct_id_long,polling_location_id_long)
);

CREATE TABLE precinct_long (
election_administration_id_long varchar(255),
ballot_style_image_url varchar(255),
electoral_district_id varchar(255),
early_vote_site_id int4,
name varchar(255),
state_id_long varchar(255),
polling_location_id_long varchar(255),
number varchar(20),
id_long varchar(255),
source text,
locality_id varchar(255),
mail_only bool,
is_split bool,
ward varchar(50),
id int4 DEFAULT nextval('pksq'),
parent_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE electoral_district__precinct_long (
electoral_district_id_long varchar(255),
precinct_id_long varchar(255),
PRIMARY KEY (electoral_district_id_long,precinct_id_long)
);

CREATE TABLE precinct__early_vote_site_long (
early_vote_site_id_long varchar(255),
precinct_id_long varchar(255),
PRIMARY KEY (precinct_id_long,early_vote_site_id_long)
);

CREATE TABLE geo_ss_long (
source text,
id int4 DEFAULT nextval('pksq'),
electoral_district_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE geo_sh_long (
source text,
id int4 DEFAULT nextval('pksq'),
electoral_district_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE ballot_response_long (
text varchar(255),
source text,
sort_order varchar(255),
id int4 DEFAULT nextval('pksq'),
contest_id_long varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE early_vote_site_long (
state_id_long varchar(255),
name varchar(255),
end_date date,
id_long varchar(255),
start_date date,
source text,
address_long varchar(255),
voter_services varchar(255),
directions varchar(255),
days_time_open varchar(255),
id int4 DEFAULT nextval('pksq'),
PRIMARY KEY (id)
);

CREATE TABLE street_segment_long (
precinct_id_long varchar(255),
start_house_number int4,
non_house_address_long varchar(255),
source text,
precinct_split_id_long varchar(255),
end_house_number int4,
odd_even_both oddevenenum,
end_apartment_number varchar(20),
id int4 DEFAULT nextval('pksq'),
start_apartment_number varchar(20),
PRIMARY KEY (id) ,
CONSTRAINT "street_segment__id" UNIQUE (id)
);

CREATE TABLE election_official_long (
fax varchar(50),
name varchar(255),
phone varchar(50),
title varchar(255),
id int4 DEFAULT nextval('pksq'),
source text,
id_long varchar(255),
email varchar(255),
PRIMARY KEY (id)
);

CREATE TABLE org_custom_field_long (
source_pk varchar(255),
parent_id int4,
type CFenum,
org_id int4,
value varchar(255),
PRIMARY KEY (parent_id,source_pk)
);

