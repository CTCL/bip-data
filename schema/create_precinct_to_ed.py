import time

def create_joined(state_abrv, connection):
    print "Creating join for {state}".format(state=state_abrv)
    t = time.time()
    connection.cursor().execute("drop table if exists precinct_locality__electoral_district_{state}VF_2012".format(state=state_abrv))
    connection.cursor().execute("create table precinct_locality__electoral_district_{state}VF_2012 as select precinct.name as precinct_name, precinct.number as precinct_number, locality.name as locality_name, electoral_district.name as electoral_district_name, electoral_district.type as electoral_district_type from precinct_{state}VF_2012 as precinct join locality_{state}VF_2012 as locality on precinct.locality_id = locality.id join electoral_district__precinct_{state}VF_2012 as edp on precinct.id = edp.precinct_id join electoral_district_{state}VF_2012 as electoral_district on edp.electoral_district_id = electoral_district.id;".format(state=state_abrv))
    print "elapsed: {time}".format(time=(time.time()-t))
    print "Creating distinct for {state}".format(state=state_abrv)
    t = time.time()
    connection.cursor().execute("drop table if exists distinct_precinct_locality__electoral_district_{state}VF_2012".format(state=state_abrv))
    connection.cursor().execute("create table distinct_precinct_locality__electoral_district_{state}VF_2012 as select distinct * from precinct_locality__electoral_district_{state}vf_2012;".format(state=state_abrv))
    print "elapsed: {time}".format(time=(time.time()-t))

def make_counts(state_abrv, connection):
    t = time.time()
    print "Making counts for {state}".format(state=state_abrv)
    connection.cursor().execute("drop table if exists temp_count_precinct_locality__electoral_district_{state}VF_2012".format(state=state_abrv))
    connection.cursor().execute("create table temp_count_precinct_locality__electoral_district_{state}VF_2012 as select precinct_name, precinct_number, locality_name, electoral_district_type, count(electoral_district_type) as count from distinct_precinct_locality__electoral_district_{state}vf_2012  group by precinct_name, precinct_number, locality_name, electoral_district_type order by locality_name, precinct_name, precinct_number;".format(state=state_abrv))

    connection.cursor().execute("drop table if exists count_distinct_precinct_locality__electoral_district_{state}VF_2012".format(state=state_abrv))
    connection.cursor().execute("create table count_distinct_precinct_locality__electoral_district_{state}VF_2012 as select a.*, b.count from temp_count_precinct_locality__electoral_district_{state}VF_2012 as b join distinct_precinct_locality__electoral_district_{state}VF_2012 as a on a.locality_name = b.locality_name and a.precinct_name = b.precinct_name and a.precinct_number = b.precinct_number and a.electoral_district_type = b.electoral_district_type;".format(state=state_abrv))
    print "elapsed: {time}".format(time=(time.time() -t))
