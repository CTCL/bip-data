from pipeline.feedripper import do_expat
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



