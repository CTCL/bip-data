from feedripper.rip import do_expat
#from pipeline.candidate import via_dict




class State:
"""
	Generic class that represents a US State: It holds the control 
	flow together that state in a way where things can be overriden 
	easily. Going to have a class for each state that is instantiated 
	directly.

	Not sure about this concept: It feels turbulent. -SF
"""
	def _get_candidate_data(self):
		yield None
	def _get_feed_path(self):
		return 'data/vip_feeds/vipFeed-testva.xml'

	def push_feed_data(self):
		ripper = do_expat()
		ripper.send(self._get_feed_path())
	def push_spatial_data(self):
		pass
	def push_candidate_data():
		for cdata in self._get_candidate_data():
			via_dict.send(cdata)
	def build(self):
		clean_state_from_db()
		push_state_data()
		push_candidate_data()

class StateBase:

	processing_steps = list()


	def add_step(self, step):
		processing_steps.add(step);

	def process(self, start_input):
		final_process = start_input

		for right in processing_steps.reverse:
			final_process = right(final_process)


ohio = StateBase()
ohio.add_step(mysql_qm)
ohio.add_step(convert_to_sql)
ohio.process(conn)


def mysql_qm(connection):
	try:
		while True:
			q = (yield)
			connection.cursor.execute(q)
	except GeneratorExit:
		connection.close()

def convert_to_sql(querymachine):
	try:
		while True:
			data = (yield)
			#transform logic
			q = make_query(data)
			querymachine.send(q)
	except GeneratorExit:
		connection.close()


pipeline = convert_to_sql(mysql_qm(conn))





wwwlog     = open("access-log")
bytecolumn = (line.rsplit(None,1)[1] for line in wwwlog)
bytes      = (int(x) for x in bytecolumn if x != '-')
bytes = (2*x for x in bytes)

print "Total", sum(bytes)



class Step:

	def act(*arg, **kwargs):
		pass


class GetCandidateDataStep(Step):
	def act(*arg, **kwargs):
		super(Step, self, *arg, **kwargs)
		return 



