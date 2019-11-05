'''
A parser for the **harm syntax based on regular expressions

Copyright (c) 2019, Néstor Nápoles
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import re
import argparse
import pprint as pp

tpc = {
(0,10): 'C--',
(0,11): 'C-',
(0,0): 'C',
(0,1): 'C#',
(0,2): 'C##',
(1,0): 'D--',
(1,1): 'D-',
(1,2): 'D',
(1,3): 'D#',
(1,4): 'D##',
(2,2): 'E--',
(2,3): 'E-',
(2,4): 'E',
(2,5): 'E#',
(2,6): 'E##',
(3,3): 'F--',
(3,4): 'F-',
(3,5): 'F',
(3,6): 'F#',
(3,7): 'F##',
(4,5): 'G--',
(4,6): 'G-',
(4,7): 'G',
(4,8): 'G#',
(4,9): 'G##',
(5,7): 'A--',
(5,8): 'A-',
(5,9): 'A',
(5,10): 'A#',
(5,11): 'A##',
(6,9): 'B--',
(6,10): 'B-',
(6,11): 'B',
(6,0): 'B#',
(6,1): 'B##'
}

tpcr = {
'C--': (0,10),
'C-': (0,11),
'C': (0,0),
'C#': (0,1),
'C##': (0,2),
'D--': (1,0),
'D-': (1,1),
'D': (1,2),
'D#': (1,3),
'D##': (1,4),
'E--': (2,2),
'E-': (2,3),
'E': (2,4),
'E#': (2,5),
'E##': (2,6),
'F--': (3,3),
'F-': (3,4),
'F': (3,5),
'F#': (3,6),
'F##': (3,7),
'G--': (4,5),
'G-': (4,6),
'G': (4,7),
'G#': (4,8),
'G##': (4,9),
'A--': (5,7),
'A-': (5,8),
'A': (5,9),
'A#': (5,10),
'A##': (5,11),
'B--': (6,9),
'B-': (6,10),
'B': (6,11),
'B#': (6,0),
'B##': (6,1)
}

class HarmKey:
    ''' Holds operations for diatonic keys '''
    def __init__(self, key='C'):
        self.setKey(key)

    def setKey(self, key):
        self.tonic = key
        self.mode = self.getMode()
        self.tpc = tpcr[self.tonic.upper()]
        self.d = self.tpc[0]
        self.p = self.tpc[1]
        self.computeDegrees()
        self.scale = [self.i, self.ii, self.iii, self.iv, self.v, self.vi, self.vii]

    def getMode(self):
        # Only check the first character
        c = self.tonic[0]
        if c.islower():
            mode = 'minor'
        elif c.isupper():
            mode = 'major'
        return mode

    def label2tpc(label):
        return tpcr[label]

    def computeDegrees(self):
        # I
        self.i = tpc[self.tpc]
        # II
        iid = (self.d+1)%7
        iip = (self.p+2)%12
        ii = (iid,iip)
        self.ii = tpc[ii]
        # III
        iiid = (self.d+2)%7
        # Different for major and minor mode
        if self.mode == 'major':
            iiip = (self.p+4)%12
        else:
            iiip = (self.p+3)%12
        iii = (iiid,iiip)
        self.iii = tpc[iii]
        # IV
        ivd = (self.d+3)%7
        ivp = (self.p+5)%12
        iv = (ivd,ivp)
        self.iv = tpc[iv]
        # V
        vd = (self.d+4)%7
        vp = (self.p+7)%12
        v = (vd,vp)
        self.v = tpc[v]
        # VI
        vid = (self.d+5)%7
        # Different for major and minor mode
        if self.mode == 'major':
            vip = (self.p+9)%12
        else:
            vip = (self.p+8)%12
        vi = (vid,vip)
        self.vi = tpc[vi]
        # VII
        viid = (self.d+6)%7
        viip = (self.p+11)%12
        vii = (viid,viip)
        self.vii = tpc[vii]
        # Neapolitan
        nd = (self.d+1)%7
        np = (self.p+1)%12
        n = (nd,np)
        self.n = tpc[n]
        # Augmented sixth chords
        ltgnfrd = (self.d+3)%7
        ltgnfrp = (self.p+6)%12
        ltgnfr = (ltgnfrd, ltgnfrp)
        self.lt = tpc[ltgnfr]
        self.gn = tpc[ltgnfr]
        self.fr = tpc[ltgnfr]
        return

class HarmDefs:
    ''' Regular expression definitions for the HarmParser class '''

    # Detect lowered or raised root (-|lowered, #|raised)
    accidental = r'''
    (?P<accidental>          # Named group _accidental
    [#-]{0,2})
    '''

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
    ([^\(^\)])+             # At least one expression
    )                       # /Group the expression
    \)                      # Closing parenthesis
    )$                      # /Match for entire string or fail
    '''

    # Detect an alternative harmony between brackets, e.g., I[V], I[V/IV], etc.
    alternative = r'''
    (\[                     # Open brackets
    (?P<alternative>        # Named group _alternative_
    ([^\[^\]])+)            # Match at least one time for any expression inside brackets
    \]                      # Close brackets
    )?                      # If no alternative expression, then no brackets should appear at all
    '''

    # Detect secondary functions, e.g., V/V, V/iv/ii, viioD7/iv/v, etc.
    secondary = r'''
    (/                      # Slash implies a secondary function
    (?P<secondary>          # Named group _secondary_
    ([\s\S])+)              # Get all the expression after the slash symbol
    )?                      # If no secondary function, then the slash symbol should not appear
    '''
    # The definition for a harm expr
    harmexpr = r'^('+accidental+roots+attribute+intervals+inversion+alternative+secondary+r')$'


class HarmParser:
    '''Parses an expression in **harm syntax'''

    defs = HarmDefs()

    def __init__(self):
        self.harmp = re.compile(HarmParser.defs.harmexpr, re.VERBOSE)
        self.impliedp = re.compile(HarmParser.defs.implied, re.VERBOSE)
        self.key = HarmKey()

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
    pp.pprint(x)
