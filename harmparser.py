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

class HarmDefs:
    ''' Regular expression definitions for the HarmParser class '''

    # The degree or special chord, i.e., I, V, Neapolitan, German augmented sixth, etc.
    roots = r'''
    (?P<root>               # Named group _root_
     i|ii|iii|iv|v|vi|vii|  # Minor mode degrees
     I|II|III|IV|V|VI|VII|  # Major mode degrees
     N|Gn|Lt|Fr|Tr)         # Special chords
    '''

    # Detect diminished or augmented triads (o|diminished, +|augmented)
    attribute = r'''
    (?P<attribute>          # Named group _attribute_
    [o+]?)
    '''

    # Detect added intervals, e.g., M7, m7, DD7, A6, etc.
    intervals = r'''
    ((?P<intervals>         # Named group _intervals
    \d+|[mMPAD]\d+|         # Detect minor, Major, Augmented or Diminished intervals
    AA\d+|                  # Double-augmented intervals
    DD\d+)                  # Double-diminished intervals
    *)                      # Not a limit on how many intervals can be added
    '''                   

    # Detect inversions (b|First inversion, c|Second inversion, d|Third inversion)
    inversion = r'''
    (?P<inversion>          # Named group _inversions_
    [b-d]?)                 # Only third inversions possible so far
    '''              

    # Detect implied harmony between parentheses, e.g., (I), (V), (viio/ii), etc.
    implied = r'''
    ^(                      # Match for entire string or fail
    \(                      # Open parenthesis
    (?P<implied_harmony>    # Group the expression
    ([\s\S])+               # At least one expression
    )                       # /Group the expression
    \)                      # Closing parenthesis
    )$                      # /Match for entire string or fail
    '''

    # Detect an alternative harmony between brackets, e.g., I[V], I[V/IV], etc.
    alternative = r'''
    (\[                     # Open brackets
    (?P<alternative>        # Named group _alternative_
    ([\s\S])+)              # Match at least one time for any expression inside brackets
    \]                      # Close brackets
    )?                      # If no alternative expression, then no brackets should appear at all
    '''                   

    # Detect secondary functions, e.g., V/V, V/iv/ii, viioD7/iv/v, etc.
    secondary = r'''
    (/                      # Slash implies a secondary function 
    (?P<secondary>           # Named group _secondary_
    ([\s\S])+)              # Get all the expression after the slash symbol
    )?                      # If no secondary function, then the slash symbol should not appear
    '''                   
    # The definition for a harm expr
    harmexpr = r'^('+roots+attribute+intervals+inversion+alternative+secondary+r')$'
    

class HarmParser:
    defs = HarmDefs()
    def __init__(self):        
        self.harmp = re.compile(HarmParser.defs.harmexpr, re.VERBOSE)
        self.impliedp = re.compile(HarmParser.defs.implied, re.VERBOSE)
    def parse(self, harmexpr):
        # Check for implied harmony
        i = self.impliedp.match(harmexpr)
        if i:
            # This is implied harmony
            impexpr = i.groupdict()['implied_harmony']     
            # Call the function again over the inner expression
            m = self.parse(impexpr)
            if m:
                m['implied'] = True
            return m
        else:
            # Normal expression
            m = self.harmp.match(harmexpr)
            if m:
                m = m.groupdict()
                m['implied'] = False
                # Finding alternative harmony
                if m['alternative'] is not None:
                    altexpr = m['alternative']
                    a = self.parse(altexpr)
                    m['alternative'] = a
                # Finding secondary functions
                if m['secondary'] is not None:
                    secexpr = m['secondary']
                    s = self.parse(secexpr)
                    m['secondary'] = s
            return m


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parses an expression in **harm syntax and describes its content')
    parser.add_argument('harm', metavar='harm_expression', help='Specify a **harm expression to be parsed')
    args = parser.parse_args()
    hp = HarmParser()
    x = hp.parse(args.harm)
    return x
