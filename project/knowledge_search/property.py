from collections import namedtuple


def load(path = 'property.data', sep = '=', comment = '#'):
	setting = {}
	with open(path) as f:
		for pair in f.read().split('\n'):
			pair = pair.strip()
			if pair and not pair.startswith(comment):
				field, value = pair.split(sep)
				setting[field.strip()] = value.strip()

	return ','.join(setting.keys()), setting


fields, setting = load()

Property = namedtuple('Property', fields)

p = Property(**setting)
