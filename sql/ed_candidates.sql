select ed.name, ed.type, cand.name, contest.office from candidate as cand left join candidate_in_contest as cic on cand.id = cic.candidate_id left join contest on contest.id = cic.contest_id left join electoral_district as ed on contest.electoral_district_id = ed.id;

select ed.name, ed.type, cand.name, contest.electoral_district_id from candidate as cand left join candidate_in_contest as cic on cand.id = cic.candidate_id left join contest on contest.id = cic.contest_id left join electoral_district as ed on contest.electoral_district_id = ed.id;

select contest.office, cand.name from candidate as cand left join candidate_in_contest as cic on cand.id = cic.candidate_id left join contest on contest.id = cic.contest_id order by cand.name;

select cic.contest_id, cand.name from candidate as cand join candidate_in_contest as cic on cand.id = cic.candidate_id order by cand.name;

select c.electoral_district_id_long, ed.id_long from contest_import_distinct as c left join electoral_district_import as ed on lower(c.electoral_district_id_long) = lower(ed.id_long);
