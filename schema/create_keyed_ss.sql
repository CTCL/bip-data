
create table street_segment_addy_keyed as
select ssl.id, ssl.source, ssl.start_house_number, ssl.end_house_number, ssl.odd_even_both, ssl.start_apartment_number, ssl.end_apartment_number, ssl.precinct_id_long, ssl.precinct_split_id_long, geo_address.id as non_house_address from street_segment_long as ssl left join geo_address on ssl.source_pk = geo_address.source_pk
