from states.base import StateBase
from deploy.conf import settings




from pipeline.feedripper import do_viacsv
from pipeline.feedripper import do_viabulkcsv

class State(StateBase):
    ripper = do_viacsv()
    bulk_ripper = do_viabulkcsv()
    def _get_feed_path(self):
        return 'data/vip_feeds/vipFeed-39-2012-03-06.xml'
