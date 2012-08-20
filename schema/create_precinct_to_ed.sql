
create table precinct_locality__electoral_district_NJVF_2012 as select precinct.name as precinct_name, precinct.number as precinct_number, locality.name as locality_name, electoral_district.name as electoral_district_name, electoral_district.type as electoral_district_type from precinct_NJVF_2012 as precinct join locality_NJVF_2012 as locality on precinct.locality_id = locality.id join electoral_district__precinct_NJVF_2012 as edp on precinct.id = edp.precinct_id join electoral_district_NJVF_2012 as electoral_district on edp.electoral_district_id = electoral_district.id;

create table distinct_precinct_locality__electoral_district_NJVF_2012 as select distinct * from precinct_locality__electoral_district_njvf_2012;
