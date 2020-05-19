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
		if '_optional' in schema and schema['_optional'] == True:
			return None
		# If the key is not optional, this is an error
		return 'Error: Key path "{}" missing'.format(path)

	# Find out what type the data should have
	objType = schema['_type']

	# If the type of the data doesn't correlate with the type described in the
	# schema, that's an error
	if type(data) != objType:
		return 'Error: Actual type "{}" at path "{}" does not match expected type "{}"'.format(
			type(data).__name__, path, objType.__name__)

	# If the current object is a dict, we need to recurse into it.
	if objType == dict:
		for key in schema:
			# Ignore schema keys
			if key[0] == '_':
				continue
			# For missing keys, add a dummy object so it can be handled
			# gracefully while recursing
			if not key in data:
				data[key] = None
			# Recurse into this key
			error = check(data[key], schema[key], path + '.' + key)
			# If an error was found, we don't need to keep going
			if error:
				return error

	# Lists can be validated by their elements and some length constraints
	elif objType == list:
		base = 'Error: List at path "{}"'.format(path)
		if '_len' in schema:
			if len(data) != schema['_len']:
				return '{} must be exactly {} elements long'.format(base, schema['_len'])
		if '_maxLen' in schema:
			if len(data) > schema['_maxLen']:
				return '{} must be at most {} elements long'.format(base, schema['_maxLen'])
		if '_minLen' in schema:
			if len(data) < schema['_minLen']:
				return '{} must be at least {} elements long'.format(base, schema['_minLen'])

		# If all constraints are fulfilled, we check the elements
		for i, el in enumerate(data):
			# Recurse into this element
			error = check(el, schema['_elements'], path + '[' + str(i) + ']')
			# If an error was found, we don't need to keep going
			if error:
				return error

	# For strings we can validate by pattern and length constraints
	elif objType == str:
		base = 'Error: String "{}" at path "{}"'.format(data, path)
		if '_len' in schema:
			if len(data) != schema['_len']:
				return '{} must be exactly {} chars long'.format(base, schema['_len'])
		if '_maxLen' in schema:
			if len(data) > schema['_maxLen']:
				return '{} must be at most {} chars long'.format(base, schema['_maxLen'])
		if '_minLen' in schema:
			if len(data) < schema['_minLen']:
				return '{} must be at least {} chars long'.format(base, schema['_minLen'])
		if '_re' in schema:
			if not re.search(schema['_re'], data):
				return '{} does not match pattern "{}"'.format(base, schema['_re'])

	# Integers can be validated by value limits
	elif objType == int:
		base = 'Error: Integer {} at path "{}"'.format(data, path)
		if '_max' in schema:
			if data > schema['_max']:
				return '{} must be at most {} chars long'.format(base, schema['_max'])
		if '_min' in schema:
			if data < schema['_min']:
				return '{} must be at least {} chars long'.format(base, schema['_min'])

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
