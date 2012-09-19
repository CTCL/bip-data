from util.coroutine import coroutine

@coroutine
def via_dict():
	try:
		while True:
			data = (yield)
			#print warn(pp.pformat(data))
	except GeneratorExit:
		pass
