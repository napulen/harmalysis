'''
A parser for the **harm syntax based on regular expressions

Nestor Napoles, June 2017
'''

import re
import argparse
import pprint as pp

tokens = [
	'i',
	'ii',
	'iii',
	'iv',
	'v',
	'vi',
	'vii',
	'I',
	'II',
	'III',
	'IV',
	'V',
	'VI',
	'VII',
	'N',
	'Gn',
	'Lt',
	'Fr',
	'Tr'
	]


def parseHarmExpr(harmexpr):
	# Discard this is an implied harmony
	p = re.compile(r'''
		^(					# Match for entire string or fail
		\(					# Open parenthesis
		(?P<implied_harmony># Group the expression
		([^\]*])+			# At least one expression
		)					# /Group the expression
		\)					# Closing parenthesis
		)$					# /Match for entire string or fail
		''', re.VERBOSE)
	i = p.match(harmexpr)
	if not i:
		# We are good to go, this is not an implied harmony, e.g., (V)
		# First group of the token, the degree (or special chord, i.e., Neapolitan, German augmented sixth, etc.)
		roots = r'{}'.format(tokens[0])
		for token in tokens:
			roots += '|{}'.format(token)	
		# Second group, augmented or diminished triads
		chordAttribute = r'[o+]?'
		# Third group, added intervals
		intervals = r'(\d+|[mMPAD]\d+|AA\d+|DD\d+)*'
		# Fourth group, inversions
		# So far, only inversions for triad or seventh chords are accepted
		inversions = r'[b-d]?'
		p = re.compile(r'''
			(									# Match the entire string or fail
			(?P<root>{})						# Get the root
			(?P<attribute>{})					# Get diminished or augmented
			(?P<intervals>{})					# Get added intervals
			(?P<inversion>{})					# Get inversion
			(\[(?P<alternative>([^\]*])+)\])?	# Parse a possible alternative expression
			)									# /Match the entire string or fail
			'''.format(roots, chordAttribute, intervals, inversions), re.VERBOSE)
		m = p.match(harmexpr)
		if m:			
			harmdict = m.groupdict()
			if 'alternative' in harmdict:
				if harmdict['alternative'] is not None:
					# An additional parsing needed, the alternative harmony									
					altdict = parseHarmExpr(harmdict['alternative'])
					# Save its dictionary instead of the string
					harmdict['alternative'] = altdict
		else:
			return None
	else:
		# Implied harmony. Get the inner expression
		expr = i.groupdict()['implied_harmony']		
		# Call the function again over the inner expression
		harmdict = parseHarmExpr(expr)
		harmdict['implied'] = True
	return harmdict
	

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses an expression in **harm syntax and describes its content')
    parser.add_argument('harmexpr', metavar='harm_expression', help='Specify a harm expression to be parsed')
    args = parser.parse_args()
    harmdict = parseHarmExpr(args.harmexpr)
    if not harmdict:
    	print 'Invalid **harm expression'
    else:
    	pp.pprint(harmdict)