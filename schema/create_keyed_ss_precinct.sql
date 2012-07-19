
create table street_segment_addy_precinct_keyed as
select ssl.id, ssl.source, ssl.start_house_number, ssl.end_house_number, ssl.odd_even_both, ssl.start_apartment_number, ssl.end_apartment_number, ssl.precinct_split_id_long, ssl.non_house_address, precinct_long.id as precinct_id from street_segment_long as ssl left join precinct_long on ssl.precinct_id_long = precinct_long.source_pk
