
import hashlib
#def intake_file(path):
#	pass
#def get_by_hash(hash):
#	pass
#def get_file_history(path):
#	pass


def open_versioned_file(path,mode):
	'''
		Versioned soure data files will all be tracked by hash.
		This mimics the interface until a well though out 
		versioning system is implemented.
	'''
	h = hashlib.sha224()
	with open(path,'rb') as f: 
	    for chunk in iter(lambda: f.read(128*h.block_size), ''): 
	         h.update(chunk)
	return (h.hexdigest(),open(path,mode)
