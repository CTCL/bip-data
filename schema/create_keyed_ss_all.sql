
create table street_segment_keyed as
select ssl.id, ssl.source, ssl.start_house_number, ssl.end_house_number, ssl.odd_even_both, ssl.start_apartment_number, ssl.end_apartment_number, precinct_long.id as precinct_id, ssl.precinct_split_id_long, geo_address.id as non_house_address from street_segment_long as ssl left join geo_address on ssl.source_pk = geo_address.source_pk left join precinct_long on ssl.precinct_id_long = precinct_long.source_pk
