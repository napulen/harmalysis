'''
The harmalysis language for harmonic analysis and roman numerals

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

from lark import Lark, tree, Transformer, v_args
import common
import interval
import harmalysis_classes
import sys

def _tertian_chord(triad, missing_intervals, inversion_by_number=None, inversion_by_letter=None, added_interval=None):
     tertian = harmalysis_classes.TertianChord()
     triad_quality, scale_degree, alteration = triad
     tertian.scale_degree = scale_degree
     tertian.scale_degree_alteration = alteration
     tertian.set_triad_quality(triad_quality)

     if inversion_by_number:
          tertian.set_inversion_by_number(inversion_by_number)
     elif inversion_by_letter:
          tertian.set_inversion_by_letter(inversion_by_letter)

     diatonic_intervals = []

     if added_interval:
          if isinstance(added_interval, interval.IntervalSpelling):
               tertian.add_interval(added_interval)
          else:
               if added_interval == 7:
                    diatonic_intervals = [7]
               elif added_interval == 9:
                    diatonic_intervals = [7, 9]
               elif added_interval == 11:
                    diatonic_intervals = [7, 9, 11]
               elif added_interval == 13:
                    diatonic_intervals = [7, 9, 11, 13]

     for i in missing_intervals:
          tertian.missing_interval(int(i))
     
     return (tertian, diatonic_intervals)

def _harmalysis():
     '''hi'''


@v_args(inline=True)
class RomanParser(Transformer):
     ##################
     ## Parsing the key
     ##################
     # Key scales
     major_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'major')
     major_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'major')
     default_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'default_minor')
     default_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'default_minor')
     natural_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'natural_minor')
     natural_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'natural_minor')
     harmonic_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'harmonic_minor')
     harmonic_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'harmonic_minor')
     melodic_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'ascending_melodic_minor')
     melodic_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'ascending_melodic_minor')
     # Key types
     key_as_reference = lambda self, _: 'reference'
     key_as_established = lambda self, _: 'established'
     # Key
     key = lambda self, key_definition, key_function: (key_definition, key_function)

     ##########################
     ## Parsing a tertian chord
     ##########################
     # Triad
     major_triad = lambda self, scale_degree: ('major_triad', str(scale_degree), None)
     major_triad_with_alteration = lambda self, alteration, scale_degree: ('major_triad', str(scale_degree), str(alteration))
     minor_triad = lambda self, scale_degree: ('minor_triad', str(scale_degree), None)
     minor_triad_with_alteration = lambda self, alteration, scale_degree: ('minor_triad', str(scale_degree), str(alteration))
     augmented_triad = lambda self, scale_degree, _: ('augmented_triad', str(scale_degree), None)
     augmented_triad_with_alteration = lambda self, alteration, scale_degree, _: ('augmented_triad', str(scale_degree), str(alteration))
     diminished_triad = lambda self, scale_degree, _: ('diminished_triad', str(scale_degree), None)
     diminished_triad_with_alteration = lambda self, alteration, scale_degree, _: ('diminished_triad', str(scale_degree), str(alteration))
     # Inversions by number
     triad_inversion_by_number = int
     seventhchord_inversion_by_number = int
     # Inversions by letter
     inversion_by_letter = str
     # Added intervals
     added_seventh_diatonic = int
     added_seventh_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_ninth_diatonic = int
     added_ninth_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_eleventh_diatonic = int
     added_eleventh_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_thirteenth_diatonic = int
     added_thirteenth_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     # Missing intervals
     missing_intervals_triad = list
     missing_intervals_seventhchord = list
     missing_intervals_ninthchord = list
     missing_intervals_eleventhchord = list
     missing_intervals_thirteenthchord = list
     # Tertian
     tertian_triad = lambda self, triad, missing_intervals: _tertian_chord(triad, missing_intervals)
     tertian_triad_with_inversion_by_number = lambda self, triad, inversion_by_number, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_number=inversion_by_number)
     tertian_seventh_with_inversion_by_number = lambda self, triad, inversion_by_number, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_number=inversion_by_number, added_interval=7)
     tertian_triad_with_inversion_by_letter = lambda self, triad, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter)
     tertian_seventh = lambda self, triad, added_seventh, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_seventh)
     tertian_seventh_with_inversion_by_letter = lambda self, triad, added_seventh, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_seventh)
     tertian_ninth = lambda self, triad, added_ninth, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_ninth)
     tertian_ninth_with_inversion_by_letter = lambda self, triad, added_ninth, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_ninth)
     tertian_eleventh = lambda self, triad, added_eleventh, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_eleventh)
     tertian_eleventh_with_inversion_by_letter = lambda self, triad, added_eleventh, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_eleventh)
     tertian_thirteenth = lambda self, triad, added_thirteenth, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_thirteenth)
     tertian_thirteenth_with_inversion_by_letter = lambda self, triad, added_thirteenth, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_thirteenth)
     #############################
     ## Parsing a harmalysis entry
     #############################
     def harmalysis_tertian(self, tertian):
          "print(sys._getframe().f_code.co_name, tertian)"

     def harmalysis_tertian_with_key(self, key, tertian):
          "print(sys._getframe().f_code.co_name, key, tertian)"
          harmalysis = harmalysis_classes.Harmalysis()
          key, function = key
          if function == 'reference':
               harmalysis.reference_key = key
          elif function == 'established':
               harmalysis.established_key = key
          tertian_chord, diatonic_intervals = tertian
          scale_degree = tertian_chord.scale_degree
          root_diatonic_step = common.roman_to_int[scale_degree]
          tertian_chord.root = getattr(key, scale_degree)
          for diatonic in diatonic_intervals:
               interval = key.mode.step_to_interval_spelling(diatonic, mode=root_diatonic_step)
               tertian_chord.add_interval(interval)
          harmalysis.chord = tertian_chord
          return harmalysis

     def harmalysis_tertian_with_tonicization(self, tertian, tonicization):
          "print(sys._getframe().f_code.co_name, tertian, tonicization)"

     def harmalysis_tertian_with_key_and_tonicization(self, key, tertian, tonicization):
          "print(sys._getframe().f_code.co_name, key, tertian, tonicization)"

grammarfile = 'harmalysis_roman.lark'
parser = Lark(open(grammarfile).read())

def parse(query, full_tree=False):
     ast = parser.parse(query)
     if full_tree:
          return ast
     return RomanParser().transform(ast)

if __name__ == '__main__':
     ast = parse(sys.argv[1], full_tree=True)
     print(RomanParser().transform(ast))
     tree.pydot__tree_to_png(ast, 'harmalysis_roman.png')