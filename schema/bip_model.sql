CREATE TYPE contestenum AS ENUM ('candidate','referendum','custom');
CREATE TYPE cfenum AS ENUM ('candidate','referendum ');
CREATE TYPE electionenum AS ENUM ('primary','general','state','Primary','General','State');
CREATE TYPE oddevenenum AS ENUM ('odd','even','both','BOTH','EVEN','ODD');
CREATE TYPE usstate AS ENUM ('AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MH', 'MA', 'MI', 'FM', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY');
CREATE SEQUENCE pksq START 1;

CREATE TABLE "election" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"date" date,
"election_type" electionenum,
"state_id" int4,
"statewide" bool,
"registration_info" varchar(255),
"absentee_ballot_info" varchar(255),
"results_url" varchar(255),
"polling_hours" varchar(255),
"election_day_registration" bool,
"registration_deadline" varchar(255),
"absentee_request_deadline" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "contest" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"election_id" int4,
"electoral_district_id" int4,
"partisan" bool,
"type" varchar(255),
"primary_party" varchar(255),
"electorate_specifications" varchar(255),
"special" bool,
"office" varchar(255),
"filing_closed_date" date,
"number_elected" int4,
"number_voting_for" int4,
"ballot_placement" varchar(255),
"contest_type" contestenum,
"write_in" bool,
"custom_ballot_heading" text,
PRIMARY KEY ("id") 
);

CREATE TABLE "candidate" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"name" varchar(255),
"party" varchar(255),
"candidate_url" varchar(255),
"biography" varchar(255),
"phone" varchar(255),
"photo_url" varchar(255),
"filed_mailing_address" int4,
"email" varchar(255),
"incumbent" bool,
"google_plus_url" varchar(255),
"twitter_name" varchar(255),
"facebook_url" varchar(255),
"wiki_word" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "referendum" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"title" varchar(255),
"subtitle" varchar(255),
"brief" varchar(255),
"text" varchar(255),
"pro_statement" varchar(255),
"con_statement" varchar(255),
"contest_id" int4,
"passage_threshold" varchar(255),
"effect_of_abstain" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "ballot_response" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"contest_id" int4,
"sort_order" varchar(255),
"text" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "candidate_in_contest" (
"sort_order" int4,
"contest_id" int4,
"candidate_id" int4,
PRIMARY KEY ("contest_id", "candidate_id") 
);

CREATE TABLE "source" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"user_id" int4,
"source_data_file_url" varchar(255),
"organization_url" varchar(255),
"name" varchar(255),
"description" text,
"hash" varchar(255),
"acquired" timestamp,
"reviewed" bool,
"reviewing_user_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "precinct" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"is_split" bool,
"parent_id" int4,
"name" varchar(255),
"number" varchar(20),
"electoral_district_id" varchar(255),
"ward" varchar(50),
"mail_only" bool,
"polling_location_id" int4,
"early_vote_site_id" int4,
"ballot_style_image_url" varchar(255),
"election_administration_id" int4,
"state_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "electoral_district" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"name" varchar(255),
"type" varchar(255),
"number" int4,
"state_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "street_segment" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"start_house_number" int4,
"end_house_number" int4,
"odd_even_both" oddevenenum,
"start_apartment_number" varchar(20),
"end_apartment_number" varchar(20),
"non_house_address" int4,
"precinct_id" int4,
"precinct_split_id" int4,
PRIMARY KEY ("id") ,
CONSTRAINT "street_segment__id" UNIQUE ("id")
);

CREATE TABLE "geo_cd" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"electoral_district_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "electoral_district__precinct" (
"electoral_district_id" int4,
"precinct_id" int4,
PRIMARY KEY ("electoral_district_id", "precinct_id") 
);

CREATE TABLE "org_custom_field" (
"parent_id" int4,
"source_pk" varchar(255),
"value" varchar(255),
"type" CFenum,
"org_id" int4,
PRIMARY KEY ("parent_id", "source_pk") 
);

CREATE TABLE "election_administration" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"name" varchar(255),
"ovc_id" int4,
"eo_id" int4,
"physical_address" int4,
"mailing_address" int4,
"elections_url" varchar(255),
"type" varchar(255),
"state_id" int4,
"hours" varchar(255),
"voter_services" varchar(255),
"rules_url" varchar(255),
"what_is_on_my_ballot_url" varchar(255),
"where_do_i_vote_url" varchar(255),
"absentee_url" varchar(255),
"am_i_registered_url" varchar(255),
"registration_url" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "state" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"name" varchar(50),
"postal_code" varchar(2),
PRIMARY KEY ("id") ,
CONSTRAINT "unique_name" UNIQUE ("name"),
CONSTRAINT "unique_postal_code" UNIQUE ("postal_code")
);

CREATE TABLE "precinct__early_vote_site" (
"precinct_id" int4,
"early_vote_site_id" int4,
PRIMARY KEY ("precinct_id", "early_vote_site_id") 
);

CREATE TABLE "early_vote_site" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"name" varchar(255),
"address" int4,
"directions" varchar(255),
"voter_services" varchar(255),
"start_date" date,
"end_date" date,
"state_id" int4,
"days_time_open" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "polling_location" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"address" int4,
"directions" varchar(255),
"polling_hours" varchar(255),
"photo_url" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "precinct__polling_location" (
"precinct_id" int4,
"polling_location_id" int4,
PRIMARY KEY ("precinct_id", "polling_location_id") 
);

CREATE TABLE "geo_county" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"electoral_district_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "geo_ss" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"electoral_district_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "geo_sh" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"electoral_district_id" int4,
PRIMARY KEY ("id") 
);

CREATE TABLE "geo_address" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"is_standardized" bool,
"is_geocoded" bool,
"house_number" int4,
"house_number_prefix" varchar(50),
"house_number_suffix" varchar(50),
"street_name" varchar(50),
"street_direction" varchar(50),
"street_suffix" varchar(50),
"address_direction" varchar(50),
"location_name" varchar(255),
"line3" varchar(255),
"line2" varchar(255),
"line1" varchar(255),
"city" varchar(255),
"state" varchar(255),
"zip4" varchar(4),
"zip" varchar(10),
"xcoord" varchar(255),
"ycoord" varchar(255),
"apartment" varchar(255),
PRIMARY KEY ("id") 
);

CREATE TABLE "election_official" (
"id" int4 DEFAULT nextval('pksq'),
"source_pk" varchar(255),
"source" text,
"title" varchar(255),
"phone" varchar(50),
"fax" varchar(50),
"email" varchar(255),
"name" varchar(255),
PRIMARY KEY ("id") 
);


ALTER TABLE "candidate_in_contest" ADD CONSTRAINT "fk_candidate__contest_contest_1" FOREIGN KEY ("contest_id") REFERENCES "contest" ("id");
ALTER TABLE "candidate_in_contest" ADD CONSTRAINT "fk_candidate__contest_candidate_1" FOREIGN KEY ("candidate_id") REFERENCES "candidate" ("id");
ALTER TABLE "contest" ADD CONSTRAINT "fk_contest_election_1" FOREIGN KEY ("election_id") REFERENCES "election" ("id");
ALTER TABLE "ballot_response" ADD CONSTRAINT "fk_ballot_response_contest_1" FOREIGN KEY ("contest_id") REFERENCES "contest" ("id");
ALTER TABLE "referendum" ADD CONSTRAINT "fk_referendum_contest" FOREIGN KEY ("contest_id") REFERENCES "contest" ("id");
ALTER TABLE "street_segment" ADD CONSTRAINT "street_segment__fk__precinct_id" FOREIGN KEY ("precinct_id") REFERENCES "precinct" ("id");
ALTER TABLE "street_segment" ADD CONSTRAINT "street_segment__fk__precinct_split_id" FOREIGN KEY ("precinct_split_id") REFERENCES "precinct" ("id");
ALTER TABLE "geo_cd" ADD CONSTRAINT "fk_geo_cd_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "electoral_district__precinct" ADD CONSTRAINT "fk_electoral_district__precinct_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "electoral_district__precinct" ADD CONSTRAINT "fk_electoral_district__precinct_precinct_1" FOREIGN KEY ("precinct_id") REFERENCES "precinct" ("id");
ALTER TABLE "election_administration" ADD CONSTRAINT "fk_election_administration_state_1" FOREIGN KEY ("state_id") REFERENCES "state" ("id");
ALTER TABLE "precinct" ADD CONSTRAINT "fk_precinct_election_administration_1" FOREIGN KEY ("election_administration_id") REFERENCES "election_administration" ("id");
ALTER TABLE "election" ADD CONSTRAINT "fk_election_state_1" FOREIGN KEY ("state_id") REFERENCES "state" ("id");
ALTER TABLE "precinct__early_vote_site" ADD CONSTRAINT "fk_precinct__early_vote_site_precinct_1" FOREIGN KEY ("precinct_id") REFERENCES "precinct" ("id");
ALTER TABLE "early_vote_site" ADD CONSTRAINT "fk_early_vote_site_state_1" FOREIGN KEY ("state_id") REFERENCES "state" ("id");
ALTER TABLE "precinct" ADD CONSTRAINT "fk_precinct_state_1" FOREIGN KEY ("state_id") REFERENCES "state" ("id");
ALTER TABLE "precinct__early_vote_site" ADD CONSTRAINT "fk_precinct__early_vote_site_early_vote_site_1" FOREIGN KEY ("early_vote_site_id") REFERENCES "early_vote_site" ("id");
ALTER TABLE "precinct__polling_location" ADD CONSTRAINT "fk_precinct__polling_location_precinct_1" FOREIGN KEY ("precinct_id") REFERENCES "precinct" ("id");
ALTER TABLE "precinct__polling_location" ADD CONSTRAINT "fk_precinct__polling_location_polling_location_1" FOREIGN KEY ("polling_location_id") REFERENCES "polling_location" ("id");
ALTER TABLE "geo_county" ADD CONSTRAINT "fk_geo_county_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "geo_ss" ADD CONSTRAINT "fk_geo_ss_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "geo_sh" ADD CONSTRAINT "fk_geo_sh_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "polling_location" ADD CONSTRAINT "fk_polling_location_geo_address_1" FOREIGN KEY ("address") REFERENCES "geo_address" ("id");
ALTER TABLE "street_segment" ADD CONSTRAINT "fk_street_segment_geo_address_1" FOREIGN KEY ("non_house_address") REFERENCES "geo_address" ("id");
ALTER TABLE "early_vote_site" ADD CONSTRAINT "fk_early_vote_site_geo_address_1" FOREIGN KEY ("address") REFERENCES "geo_address" ("id");
ALTER TABLE "election_administration" ADD CONSTRAINT "fk_election_administration_geo_address_1" FOREIGN KEY ("physical_address") REFERENCES "geo_address" ("id");
ALTER TABLE "election_administration" ADD CONSTRAINT "fk_election_administration_geo_address_2" FOREIGN KEY ("mailing_address") REFERENCES "geo_address" ("id");
ALTER TABLE "election_administration" ADD CONSTRAINT "fk_election_administration_election_official_1" FOREIGN KEY ("ovc_id") REFERENCES "election_official" ("id");
ALTER TABLE "election_administration" ADD CONSTRAINT "fk_election_administration_election_official_2" FOREIGN KEY ("eo_id") REFERENCES "election_official" ("id");
ALTER TABLE "contest" ADD CONSTRAINT "fk_contest_electoral_district_1" FOREIGN KEY ("electoral_district_id") REFERENCES "electoral_district" ("id");
ALTER TABLE "candidate" ADD CONSTRAINT "fk_candidate_geo_address_1" FOREIGN KEY ("filed_mailing_address") REFERENCES "geo_address" ("id");
ALTER TABLE "precinct" ADD CONSTRAINT "fk_precinct_split_precinct_1" FOREIGN KEY ("parent_id") REFERENCES "precinct" ("id");
ALTER TABLE "electoral_district" ADD CONSTRAINT "fk_electoral_district_state_1" FOREIGN KEY ("state_id") REFERENCES "state" ("id");
