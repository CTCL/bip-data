# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order (DONE)
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
class State(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=20, unique=True, blank=True)
    postal_code = models.CharField(max_length=2, unique=True, blank=True)
    class Meta:
        db_table = u'state'

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    election_type = models.TextField(blank=True) # This field type is a guess.
    state = models.ForeignKey(State, null=True, blank=True)
    statewide = models.BooleanField(null=True, blank=True)
    registration_info = models.CharField(max_length=255, blank=True)
    absentee_ballot_info = models.CharField(max_length=255, blank=True)
    results_url = models.CharField(max_length=255, blank=True)
    polling_hours = models.CharField(max_length=255, blank=True)
    election_day_registration = models.BooleanField(null=True, blank=True)
    registration_deadline = models.CharField(max_length=255, blank=True)
    absentee_request_deadline = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'election'

class ElectoralDistrict(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'electoral_district'

class Contest(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    election = models.ForeignKey(Election, null=True, blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    partisan = models.BooleanField(null=True, blank=True)
    type = models.CharField(max_length=255, blank=True)
    primary_party = models.CharField(max_length=255, blank=True)
    electorate_specifications = models.CharField(max_length=255, blank=True)
    special = models.BooleanField(null=True, blank=True)
    office = models.CharField(max_length=255, blank=True)
    filing_closed_date = models.DateField(null=True, blank=True)
    number_elected = models.IntegerField(null=True, blank=True)
    number_voting_for = models.IntegerField(null=True, blank=True)
    ballot_placement = models.CharField(max_length=255, blank=True)
    contest_type = models.TextField(blank=True) # This field type is a guess.
    write_in = models.BooleanField(null=True, blank=True)
    custom_ballot_heading = models.TextField(blank=True)
    class Meta:
        db_table = u'contest'

class BallotResponse(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    contest = models.ForeignKey(Contest, null=True, blank=True)
    sort_order = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'ballot_response'

class GeoAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    is_standardized = models.BooleanField(null=True, blank=True)
    is_geocoded = models.BooleanField(null=True, blank=True)
    house_number = models.IntegerField(null=True, blank=True)
    house_number_prefix = models.CharField(max_length=50, blank=True)
    hosue_number_suffix = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=50, blank=True)
    street_direction = models.CharField(max_length=50, blank=True)
    street_suffix = models.CharField(max_length=50, blank=True)
    address_direction = models.CharField(max_length=50, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    line3 = models.CharField(max_length=255, blank=True)
    line2 = models.CharField(max_length=255, blank=True)
    line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip4 = models.CharField(max_length=4, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    xcoord = models.CharField(max_length=255, blank=True)
    ycoord = models.CharField(max_length=255, blank=True)
    apartment = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'geo_address'



class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    party = models.CharField(max_length=255, blank=True)
    candidate_url = models.CharField(max_length=255, blank=True)
    biography = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    photo_url = models.CharField(max_length=255, blank=True)
    filed_mailing_address = models.ForeignKey(GeoAddress, null=True, db_column='filed_mailing_address', blank=True)
    email = models.CharField(max_length=255, blank=True)
    incumbent = models.BooleanField(null=True, blank=True)
    google_plus_url = models.CharField(max_length=255, blank=True)
    twitter_name = models.CharField(max_length=255, blank=True)
    facebook_url = models.CharField(max_length=255, blank=True)
    wiki_word = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'candidate'

class CandidateInContest(models.Model):
    sort_order = models.IntegerField(null=True, blank=True)
    contest = models.ForeignKey(Contest)
    candidate = models.ForeignKey(Candidate)
    class Meta:
        db_table = u'candidate_in_contest'

class Contest(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    election = models.ForeignKey(Election, null=True, blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    partisan = models.BooleanField(null=True, blank=True)
    type = models.CharField(max_length=255, blank=True)
    primary_party = models.CharField(max_length=255, blank=True)
    electorate_specifications = models.CharField(max_length=255, blank=True)
    special = models.BooleanField(null=True, blank=True)
    office = models.CharField(max_length=255, blank=True)
    filing_closed_date = models.DateField(null=True, blank=True)
    number_elected = models.IntegerField(null=True, blank=True)
    number_voting_for = models.IntegerField(null=True, blank=True)
    ballot_placement = models.CharField(max_length=255, blank=True)
    contest_type = models.TextField(blank=True) # This field type is a guess.
    write_in = models.BooleanField(null=True, blank=True)
    custom_ballot_heading = models.TextField(blank=True)
    class Meta:
        db_table = u'contest'

class EarlyVoteSite(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    address = models.ForeignKey(GeoAddress, null=True, db_column='address', blank=True)
    directions = models.CharField(max_length=255, blank=True)
    voter_services = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    days_time_open = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'early_vote_site'

class Election(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    election_type = models.TextField(blank=True) # This field type is a guess.
    state = models.ForeignKey(State, null=True, blank=True)
    statewide = models.BooleanField(null=True, blank=True)
    registration_info = models.CharField(max_length=255, blank=True)
    absentee_ballot_info = models.CharField(max_length=255, blank=True)
    results_url = models.CharField(max_length=255, blank=True)
    polling_hours = models.CharField(max_length=255, blank=True)
    election_day_registration = models.BooleanField(null=True, blank=True)
    registration_deadline = models.CharField(max_length=255, blank=True)
    absentee_request_deadline = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'election'

class ElectionOfficial(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'election_official'

class ElectionAdministration(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    ovc = models.ForeignKey(ElectionOfficial, null=True, blank=True)
    eo = models.ForeignKey(ElectionOfficial, null=True, blank=True)
    physical_address = models.ForeignKey(GeoAddress, null=True, db_column='physical_address', blank=True)
    mailing_address = models.ForeignKey(GeoAddress, null=True, db_column='mailing_address', blank=True)
    elections_url = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    hours = models.CharField(max_length=255, blank=True)
    voter_services = models.CharField(max_length=255, blank=True)
    rules_url = models.CharField(max_length=255, blank=True)
    what_is_on_my_ballot_url = models.CharField(max_length=255, blank=True)
    where_do_i_vote_url = models.CharField(max_length=255, blank=True)
    absentee_url = models.CharField(max_length=255, blank=True)
    am_i_registered_url = models.CharField(max_length=255, blank=True)
    registration_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'election_administration'

class ElectionOfficial(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'election_official'

class ElectoralDistrict(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=255, blank=True)
    number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'electoral_district'

class Precinct(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=20, blank=True)
    electoral_district_id = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    mail_only = models.BooleanField(null=True, blank=True)
    polling_location_id = models.IntegerField(null=True, blank=True)
    early_vote_site_id = models.IntegerField(null=True, blank=True)
    ballot_style_image_url = models.CharField(max_length=255, blank=True)
    election_administration = models.ForeignKey(ElectionAdministration, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    class Meta:
        db_table = u'precinct'

class ElectoralDistrictPrecinct(models.Model):
    electoral_district = models.ForeignKey(ElectoralDistrict)
    precinct = models.ForeignKey(Precinct)
    class Meta:
        db_table = u'electoral_district__precinct'

class GeoAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    is_standardized = models.BooleanField(null=True, blank=True)
    is_geocoded = models.BooleanField(null=True, blank=True)
    house_number = models.IntegerField(null=True, blank=True)
    house_number_prefix = models.CharField(max_length=50, blank=True)
    hosue_number_suffix = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=50, blank=True)
    street_direction = models.CharField(max_length=50, blank=True)
    street_suffix = models.CharField(max_length=50, blank=True)
    address_direction = models.CharField(max_length=50, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    line3 = models.CharField(max_length=255, blank=True)
    line2 = models.CharField(max_length=255, blank=True)
    line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip4 = models.CharField(max_length=4, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    xcoord = models.CharField(max_length=255, blank=True)
    ycoord = models.CharField(max_length=255, blank=True)
    apartment = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'geo_address'



class GeoCd(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    class Meta:
        db_table = u'geo_cd'

class GeoCounty(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    class Meta:
        db_table = u'geo_county'

class GeoSh(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    class Meta:
        db_table = u'geo_sh'

class GeoSs(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    electoral_district = models.ForeignKey(ElectoralDistrict, null=True, blank=True)
    class Meta:
        db_table = u'geo_ss'

class OrgCustomField(models.Model):
    parent_id = models.IntegerField()
    source_pk = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)
    type = models.TextField(blank=True) # This field type is a guess.
    org_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'org_custom_field'

class PollingLocation(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    address = models.ForeignKey(GeoAddress, null=True, db_column='address', blank=True)
    directions = models.CharField(max_length=255, blank=True)
    polling_hours = models.CharField(max_length=255, blank=True)
    photo_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'polling_location'

class Precinct(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=20, blank=True)
    electoral_district_id = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    mail_only = models.BooleanField(null=True, blank=True)
    polling_location_id = models.IntegerField(null=True, blank=True)
    early_vote_site_id = models.IntegerField(null=True, blank=True)
    ballot_style_image_url = models.CharField(max_length=255, blank=True)
    election_administration = models.ForeignKey(ElectionAdministration, null=True, blank=True)
    state = models.ForeignKey(State, null=True, blank=True)
    class Meta:
        db_table = u'precinct'

class PrecinctEarlyVoteSite(models.Model):
    precinct = models.ForeignKey(Precinct)
    early_vote_site = models.ForeignKey(EarlyVoteSite)
    class Meta:
        db_table = u'precinct__early_vote_site'

class PrecinctPollingLocation(models.Model):
    precinct = models.ForeignKey(Precinct)
    polling_location = models.ForeignKey(PollingLocation)
    class Meta:
        db_table = u'precinct__polling_location'

class Referendum(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    brief = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)
    pro_statement = models.CharField(max_length=255, blank=True)
    con_statement = models.CharField(max_length=255, blank=True)
    contest = models.ForeignKey(Contest, null=True, blank=True)
    passage_threshold = models.CharField(max_length=255, blank=True)
    effect_of_abstain = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'referendum'

class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    source_data_file_url = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    hash = models.CharField(max_length=255, blank=True)
    aquired = models.DateTimeField(null=True, blank=True)
    reviewed = models.BooleanField(null=True, blank=True)
    reviewing_user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'source'

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    name = models.CharField(max_length=20, unique=True, blank=True)
    postal_code = models.CharField(max_length=2, unique=True, blank=True)
    class Meta:
        db_table = u'state'

class StreetSegment(models.Model):
    id = models.IntegerField(primary_key=True)
    source_pk = models.CharField(max_length=255, blank=True)
    source = models.TextField(blank=True)
    start_house_number = models.IntegerField(null=True, blank=True)
    end_house_number = models.IntegerField(null=True, blank=True)
    odd_even_both = models.TextField(blank=True) # This field type is a guess.
    start_apartment_number = models.CharField(max_length=20, blank=True)
    end_apartment_number = models.CharField(max_length=20, blank=True)
    non_house_address = models.ForeignKey(GeoAddress, null=True, db_column='non_house_address', blank=True)
    precinct = models.ForeignKey(Precinct, null=True, blank=True)
    precinct_split = models.ForeignKey(Precinct, null=True, blank=True)
    class Meta:
        db_table = u'street_segment'