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
     # TODO: Currently, it only supports intervals from unison to 15th
     interval_qualities = ['P', 'M', 'M', 'P', 'P', 'M', 'M'
                           'P', 'M', 'M', 'P', 'P', 'M', 'M', 'P']
     reference_semitones = [0, 2, 4, 5, 7, 9, 11,
                           12, 14, 16, 17, 19, 21, 23, 24]
     interval_alterations = {
          # Perfect intervals (1, 4, 5, 8, 11, etc.)
          "P": {"DD": -2, "D": -1, "P": 0, "A": 1, "AA": 2},
          # Nonperfect intervals (2, 3, 6, 7, 9, 10, etc.)
          "M": {"DD": -3, "D": -2, "m": -1, "M": 0, "A": 1, "AA": 2}
     }

     def __init__(self, interval_quality, general_interval):
          interval_index = general_interval - 1
          self.interval_type = Interval.interval_qualities[interval_index]
          # A diminished interval means different things for
          # perfect intervals and nonperfect intervals
          self.interval_alteration = Interval.interval_alterations[self.interval_type][interval_quality]

class PitchClassSpelling(object):
     diatonic_classes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
     pitch_classes = [0, 2, 4, 5, 7, 9, 11]
     alterations = {
          '--': -2, 'bb': -2,
          '-':  -1, 'b':  -1,
          '#':   1,
          '##':  2, 'x':   2
     }
     def __init__(self, note_letter, alteration=None):
          if not note_letter in PitchClassSpelling.diatonic_classes:
               raise ValueError("note letter '{}' is not supported.".format(note_letter))
          self.note_letter = note_letter
          self.diatonic_class = PitchClassSpelling.diatonic_classes.index(note_letter)
          if alteration:
               if not alteration in PitchClassSpelling.alterations:
                    raise ValueError("alteration '{}' is not supported.".format(alteration))
               self.alteration = alteration
               alteration_value = PitchClassSpelling.alterations[alteration]
          else:
               self.alteration = ''
               alteration_value = 0
          default_chromatic_class = PitchClassSpelling.pitch_classes[self.diatonic_class]
          self.chromatic_class = (12 + default_chromatic_class + alteration_value) % 12

     def __str__(self):
          return '{}{}'.format(self.note_letter, self.alteration)


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


