from pipeline.feedripper import do_viacsv
import importlib
from pipeline.candidate import via_dict




class StateBase:
    """
    Generic class that represents a US State: It holds the control 
    flow together that state in a way where things can be overriden 
    easily. Going to have a class for each state that is instantiated 
    directly.

    Not sure about this concept: It feels turbulent. -SF
    """
    #Designed to be configurable
    ripper = None#configure this
    bulk_ripper = None
    def _get_feed_path(self):
        return 'data/vip_feeds/vipFeed-testva.xml'
    def _get_candidate_data(self):
        return []
    #Cleaning
    def clean_state_from_db(self):
        pass
    #Things for adding data
    def push_feed_data(self):
        self.ripper.send(self._get_feed_path())
    
    def bulk_push_feed_data(self):
        self.bulk_ripper.send(self._get_feed_path())
    
    def push_candidate_data(self):
        for cdata in self._get_candidate_data():
            via_dict.send(cdata)
    def _pre_build_hook(self):
        pass
    def _post_build_hook(self):
        pass
    #Go
    def build(self):
        self._pre_build_hook()
        self.clean_state_from_db()
        self.push_feed_data()
        self.push_candidate_data()
        self._post_build_hook()
    def bulkbuild(self):
        self._pre_build_hook()
        self.clean_state_from_db()
        self.bulk_push_feed_data()
        self.push_candidate_data()
        self._post_build_hook()



def buildstates():
    """
        Build states from the ground up. Cleans data that exists!
    """
    import sys
    state_codes = (x.lower() for x in sys.argv[1:])
    for state_code in state_codes:
        State = importlib.import_module('states.%s' % state_code).State
        #_temp = __import__('spam.ham', globals(), locals(), ['eggs', 'sausage'], -1)
        some_state = State()
        some_state.build()

def bulkbuildstates():
    """
        Build states from the ground up using bulk import.
    """
    import sys
    state_codes = (x.lower() for x in sys.argv[1:])
    for state_code in state_codes:
        State = importlib.import_module('states.%s' % state_code).State
        #_temp = __import__('spam.ham', globals(), locals(), ['eggs', 'sausage'], -1)
        some_state = State()
        some_state.bulkbuild()

