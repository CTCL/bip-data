import re


named_zip = re.compile(r'(?P<trash>[A-Z]*)(?P<zip>\d{5})-?(?P<zip4>\d{4})?')
tests_for_named_zip = ['20009','20009672','20009-6562','20009-23','VA20009-2635','VA20009-2']
