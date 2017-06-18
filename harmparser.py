'''
A parser for the **harm syntax based on regular expressions

Copyright 2017 Nestor Napoles

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

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
			^(									# Match the entire string or fail
			(?P<root>{})						# Get the root
			(?P<attribute>{})					# Get diminished or augmented
			(?P<intervals>{})					# Get added intervals
			(?P<inversion>{})					# Get inversion
			(\[(?P<alternative>([^\]*])+)\])?	# Parse a possible alternative expression
			)$									# /Match the entire string or fail
			'''.format(roots, chordAttribute, intervals, inversions), re.VERBOSE)
		m = p.match(harmexpr)
		if m:			
			harmdict = m.groupdict()
			harmdict['implied'] = False
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


def parseHarm(harm):
	# Separate possible secondary functions
	exprs = harm.split('/')
	functions = []
	for harmexpr in exprs:
		harmdict = parseHarmExpr(harmexpr)
		if not harmdict:
			print 'Invalid **harm expression: {}'.format(harmexpr)
		else:
			functions.append(harmdict)
	pp.pprint(functions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses an expression in **harm syntax and describes its content')
    parser.add_argument('harm', metavar='harm_expression', help='Specify a **harm expression to be parsed')
    args = parser.parse_args()
    harmdict = parseHarm(args.harm)
