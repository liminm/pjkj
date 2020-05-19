import json, re

from . import util

max_name_len = 42

team = {
	"_type": dict,
	"name": {
		"_type": str,
		"_re": r"^.+$",
		"_maxLen": max_name_len,
	},
	"isisName": {
		"_optional": True,
		"_type": str,
		"_re": r"^.*$",
		"_maxLen": max_name_len,
	},
	"type": {
		"_type": str,
		"_re": r"^(jumpSturdy|racingKings)$",
	},
}

player = {
	"_type": dict,
	"name": {
		"_type": str,
		"_re": r"^.+$",
		"_maxLen": max_name_len,
	},
}

game = {
	"_type": dict,
	"name": {
		"_type": str,
		"_re": r"^.+$",
		"_maxLen": max_name_len,
	},
	"type": {
		"_type": str,
		"_re": r"^(jumpSturdy|racingKings)$",
	},
	"players": {
		"_type": dict,
		"playerA": {
			"_type": str,
			"_re": r"^\w+$",
			"_len": util.id_len,
		},
		"playerB": {
			"_type": str,
			"_re": r"^\w+$",
			"_len": util.id_len,
		},
	},
	"settings": {
		"_type": dict,
		"initialFEN": {
			"_optional": True,
			"_type": str,
			"_re": r"^.+$",
			"_minLen": 10,
			"_maxLen": 100,
		},
		"timeBudget": {
			"_type": int,
			"_min": 1000,		# 1s
			"_max": 7200000,	# 2h
		},
		"timeout": {
			"_type": int,
			"_min": 100,		# .1s
			"_max": 3600000,	# 1h
		}
	}
}

event = {
	"_type": dict,
	"type": {
		"_type": str,
		"_re": r"^(move|surrender)$",
	},
	"details": {
		"_type": dict,
		"_optional": True,
		"move": {
			"_type": str,
			"_minLen": 4,
			"_maxLen": 5,
		}
	}
}

listTest = {
	"_type": list,
	"_minLen": 2,
	"_elements": {
		"_type": dict,
		"name": {
			"_type": str,
			"_minLen": 16
		}
	}
}

def check(data, schema, path = ''):

	# If a schema key is missing from the data, we have to decide between 2
	# cases:
	if data == None:
		# Keys can be optional. In that case, it's valid
		if schema.get('_optional'):
			return None
		# If the key is not optional, this is an error
		return 'Error: Key path "{}" missing'.format(path)

	# Find out what type the data should have
	_type = schema['_type']

	# If the type of the data doesn't correlate with the type described in the
	# schema, that's an error
	if type(data) != _type:
		return 'Error: Actual type "{}" at path "{}" does not match expected type "{}"'.format(
			type(data).__name__, path, _type.__name__)

	# If the current object is a dict, we need to recurse into it.
	if _type == dict:
		for key in schema:
			# Ignore schema keys
			if key[0] == '_':
				continue
			# Recurse into this key
			error = check(data.get(key), schema[key], path + '.' + key)
			# If an error was found, we don't need to keep going
			if error:
				return error

	# Lists can be validated by their elements and some length constraints
	elif _type == list:
		base = 'Error: List at path "{}"'.format(path)
		_len = schema.get('_len')
		if _len and len(data) != _len:
			return '{} must be exactly {} elements long'.format(base, _len)
		_maxLen = schema.get('_maxLen')
		if _maxLen and len(data) > _maxLen:
			return '{} must be at most {} elements long'.format(base, _maxLen)
		_minLen = schema.get('_minLen')
		if _minLen and len(data) < _minLen:
			return '{} must be at least {} elements long'.format(base, _minLen)

		# If all constraints are fulfilled, we check the elements
		for i, el in enumerate(data):
			# Recurse into this element
			error = check(el, schema['_elements'], path + '[' + str(i) + ']')
			# If an error was found, we don't need to keep going
			if error:
				return error

	# For strings we can validate by pattern and length constraints
	elif _type == str:
		base = 'Error: String "{}" at path "{}"'.format(data, path)
		_len = schema.get('_len')
		if _len and len(data) != _len:
			return '{} must be exactly {} chars long'.format(base, _len)
		_maxLen = schema.get('_maxLen')
		if _maxLen and len(data) > _maxLen:
			return '{} must be at most {} chars long'.format(base, _maxLen)
		_minLen = schema.get('_minLen')
		if _minLen and len(data) < _minLen:
			return '{} must be at least {} chars long'.format(base, _minLen)
		_re = schema.get('_re')
		if _re and not re.search(schema['_re'], data):
			return '{} does not match pattern "{}"'.format(base, _re)

	# Integers can be validated by value limits
	elif _type == int:
		base = 'Error: Integer {} at path "{}"'.format(data, path)
		_max = schema.get('_max')
		if _max and data > _max:
			return '{} must be at most {} chars long'.format(base, _max)
		_min = schema.get('_min')
		if _min and data < _min:
			return '{} must be at least {} chars long'.format(base, _min)

	return None


def parseAndCheck(payload, schema):

	# Parse JSON and check validity
	try:
		payload = payload.decode('UTF-8')
		data = json.loads(payload)
	except ValueError as e:
		return None, ['Error: JSON decode error:\n' + e, 400]

	# Check contents
	error = check(data, schema)
	if error:
		# Return error message and code `400 BAD REQUEST`
		return None, [error, 400]
	else:
		# return valid data
		return data, None
