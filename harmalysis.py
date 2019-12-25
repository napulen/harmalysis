'''
The harmalysis language for harmonic analysis and roman numerals

Copyright (c) 2019, Nestor Napoles
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

from lark import Lark, Transformer, Visitor, v_args, tree
import sys

class Interval(object):
     valid_intervals = ['DD', 'D', 'm', 'M', 'P', 'A', 'AA']
     interval_qualities = ['P', 'M', 'M', 'P', 'P', 'M', 'M']
     operations_perfect = {
          "DD": -2,
          "D": -1,
          "P": 0,
          "A": 1,
          "AA": 2
     }
     operations_nonperfect = {
          "DD": -3,
          "D": -2,
          "m": -1,
          "M": 0,
          "A": 1,
          "AA": 2
     }

class PitchClassSpelling(object):
     pcspell_from_duple = {
          (0,10): 'C--', (0,11): 'C-', (0, 0): 'C', (0, 1): 'C#', (0, 2): 'C##',
          (1, 0): 'D--', (1, 1): 'D-', (1, 2): 'D', (1, 3): 'D#', (1, 4): 'D##',
          (2, 2): 'E--', (2, 3): 'E-', (2, 4): 'E', (2, 5): 'E#', (2, 6): 'E##',
          (3, 3): 'F--', (3, 4): 'F-', (3, 5): 'F', (3, 6): 'F#', (3, 7): 'F##',
          (4, 5): 'G--', (4, 6): 'G-', (4, 7): 'G', (4, 8): 'G#', (4, 9): 'G##',
          (5, 7): 'A--', (5, 8): 'A-', (5, 9): 'A', (5,10): 'A#', (5,11): 'A##',
          (6, 9): 'B--', (6,10): 'B-', (6,11): 'B', (6, 0): 'B#', (6, 1): 'B##'
     }
     pcspell_from_string = {value: key for key, value in pcspell_from_duple.items()}
     def __init__(self, pcspell_string):
          if pcspell_string in PitchClassSpelling.pcspell_from_string:
               self.diatonic_class, self.chromatic_class = PitchClassSpelling.pcspell_from_string[pcspell_string]

@v_args(inline=True)
class HarmalysisParser(Transformer):
     ##################
     ## Parsing the key
     ##################

     # Key scales
     def major_key(self, letter):
          print(sys._getframe().f_code.co_name, letter)

     def major_key_with_alteration(self, letter, alteration):
          print('{}{}'.format(letter, alteration))

     def default_minor_key(self, letter):
          print(sys._getframe().f_code.co_name, letter)

     def default_minor_key_with_alteration(self, letter, alteration):
          print(sys._getframe().f_code.co_name, letter, alteration)

     def natural_minor_key(self, letter):
          print(sys._getframe().f_code.co_name, letter)

     def natural_minor_key_with_alteration(self, letter, alteration):
          print(sys._getframe().f_code.co_name, letter, alteration)

     def harmonic_minor_key(self, letter):
          print(sys._getframe().f_code.co_name, letter)

     def harmonic_minor_key_with_alteration(self, letter, alteration):
          print(sys._getframe().f_code.co_name, letter, alteration)

     def melodic_minor_key(self, letter):
          print(sys._getframe().f_code.co_name, letter)

     def melodic_minor_key_with_alteration(self, letter, alteration):
          print(sys._getframe().f_code.co_name, letter, alteration)

     # Key types
     def key_as_reference(self, reference):
          print(sys._getframe().f_code.co_name, reference)

     def key_as_established(self, established):
          print(sys._getframe().f_code.co_name, established)

     # Key
     def key(self, key_definition, key_function):
          print(sys._getframe().f_code.co_name)

test_strings = [
     'C:viio65',
     'f#_nat:#viiom7b|f#_nat:vii065|?e#m3D5m7',
     'f#_nat:#viiom7bx5[f#_nat=>:vii065]',
]

if __name__ == '__main__':
     grammar = 'harmalysis.lark'
     l = Lark(open(grammar).read(), start="start")
     t = l.parse(sys.argv[1])
     print(t)
     print(t.pretty())
     tree.pydot__tree_to_png(t, 'harmparser.png')
     print("Transformer")
     HarmalysisParser().transform(t)


