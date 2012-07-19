
CREATE TABLE street_segment as select fromtable.start_house_number,fromtable.source,fromtable.end_house_number,fromtable.odd_even_both,fromtable.end_apartment_number,fromtable.id,fromtable.start_apartment_number,geo_address_long.id as non_house_address,pl1.id as precinct_id,pl2.id as precinct_split_id 
from street_segment_long as fromtable left join geo_address_long on fromtable.non_house_address_long = geo_address_long.id_long left join precinct_long as pl1 on fromtable.precinct_id_long = pl1.id_long left join precinct_long as pl2 on fromtable.precinct_split_id_long = pl2.id_long;
