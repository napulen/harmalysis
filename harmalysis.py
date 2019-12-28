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

TONIC = 0
SUPERTONIC = 1
MEDIANT = 2
SUBDOMINANT = 3
DOMINANT = 4
SUBMEDIANT = 5
SEVENTH_DEGREE = 6
DIATONIC_CLASSES = 7

class IntervalSpelling(object):
     interval_qualities = ['DD', 'D', 'm', 'M', 'P', 'A', 'AA']
     # Perfect intervals (1, 4, 5, 8, 11, etc.)
     perfect_interval_alterations = {
          "DD": -2, "D": -1, "P": 0, "A": 1, "AA": 2
     }
     # Nonperfect intervals (2, 3, 6, 7, 9, 10, etc.)
     nonperfect_interval_alterations = {
          "DD": -3, "D": -2, "m": -1, "M": 0, "A": 1, "AA": 2
     }
     def __init__(self, interval_quality, diatonic_interval):
          # The diatonic classes that have a perfect interval:
          # Unison, Subdominant, Dominant, and compound
          # intervals of the same classes (8ve, 11th, 12th, 15th, etc.)
          diatonic_classes_with_perfect_intervals = [TONIC, SUBDOMINANT, DOMINANT]
          diatonic_class = (diatonic_interval - 1) % DIATONIC_CLASSES
          is_perfect_interval = diatonic_class in diatonic_classes_with_perfect_intervals
          if is_perfect_interval:
               alteration_effects = IntervalSpelling.perfect_interval_alterations
          else:
               alteration_effects = IntervalSpelling.nonperfect_interval_alterations
          if not interval_quality in alteration_effects:
               raise KeyError("interval quality '{}' is not supported".format(interval_quality))
          self.interval_quality = interval_quality
          self.diatonic_interval = diatonic_interval
          self.alteration_effect = alteration_effects[interval_quality]
          self.semitones = MajorScale().step_to_semitones(diatonic_interval) + self.alteration_effect

     def __str__(self):
          return '{}{}'.format(self.interval_quality, self.diatonic_interval)


class MajorScale(object):
     def __init__(self):
          self.scale_degree_quality = ['P', 'M', 'M', 'P', 'P', 'M', 'M']
          self.scale_degree_semitones = [0, 2, 4, 5, 7, 9, 11]

     def step_to_interval_spelling(self, step):
          self.quality = self.scale_degree_quality[(step - 1) % DIATONIC_CLASSES]
          return IntervalSpelling(self.quality, step)

     def step_to_semitones(self, step):
          octaves = (step - 1) // DIATONIC_CLASSES
          step_semitones = self.scale_degree_semitones[(step - 1) % DIATONIC_CLASSES]
          self.semitones = (12 * octaves) + step_semitones
          return self.semitones


class NaturalMinorScale(MajorScale):
     def __init__(self):
          super().__init__()
          self.scale_degree_quality[MEDIANT] = 'm'
          self.scale_degree_quality[SUBMEDIANT] = 'm'
          self.scale_degree_quality[SEVENTH_DEGREE] = 'm'
          self.scale_degree_semitones[MEDIANT] = 3
          self.scale_degree_semitones[SUBMEDIANT] = 8
          self.scale_degree_semitones[SEVENTH_DEGREE] = 10


class HarmonicMinorScale(NaturalMinorScale):
     def __init__(self):
          super().__init__()
          self.scale_degree_quality[SEVENTH_DEGREE] = 'M'
          self.scale_degree_semitones[SEVENTH_DEGREE] = 11


class AscendingMelodicMinorScale(HarmonicMinorScale):
     def __init__(self):
          super().__init__()
          self.scale_degree_quality[SUBMEDIANT] = 'M'
          self.scale_degree_semitones[SUBMEDIANT] = 9


class PitchClassSpelling(object):
     diatonic_classes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
     pitch_classes = [0, 2, 4, 5, 7, 9, 11]
     alterations = {
          '--': -2, 'bb': -2,
          '-':  -1, 'b':  -1,
          '#':   1,
          '##':  2, 'x':   2
     }
     alterations_r = {
          -2: 'bb',
          -1: 'b',
          1: '#',
          2: 'x'
     }
     def __init__(self, note_letter, alteration=None):
          note_letter = note_letter.upper()
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

     @classmethod
     def from_diatonic_chromatic_classes(cls, diatonic_class, chromatic_class):
          if  0 > diatonic_class or diatonic_class >= DIATONIC_CLASSES:
               raise ValueError("diatonic class {} is out of bounds.".format(diatonic_class))
          if  0 > diatonic_class or diatonic_class >= 12:
               raise ValueError("chromatic class {} is out of bounds.".format(chromatic_class))
          note_letter = cls.diatonic_classes[diatonic_class]
          default_pitch_class = cls.pitch_classes[diatonic_class]
          if default_pitch_class == chromatic_class:
               alteration = None
          else:
               alteration_found = False
               for alteration_effect, alteration in cls.alterations_r.items():
                    test_chromatic_class = (12 + chromatic_class - alteration_effect) % 12
                    if test_chromatic_class == default_pitch_class:
                         alteration_found = True
                         break
               if not alteration_found:
                    raise ValueError("chromatic class {} is unreachable by this diatonic class.".format(chromatic_class))
          return PitchClassSpelling(note_letter, alteration)

     def to_interval(self, interval_spelling):
          if not isinstance(interval_spelling, IntervalSpelling):
               raise TypeError('expecting IntervalSpelling instead of {}.'.format(type(interval_spelling)))
          diatonic_steps = interval_spelling.diatonic_interval - 1
          semitones = interval_spelling.semitones

          new_diatonic_class = (diatonic_steps + self.diatonic_class) % DIATONIC_CLASSES
          new_chromatic_class = (semitones + self.chromatic_class) % 12
          return PitchClassSpelling.from_diatonic_chromatic_classes(new_diatonic_class, new_chromatic_class)

     def __str__(self):
          return '{}{}'.format(self.note_letter, self.alteration)


class Key(object):
     scale_mapping = {
          "major": MajorScale(),
          "natural_minor": NaturalMinorScale(),
          "harmonic_minor": HarmonicMinorScale(), "default_minor": HarmonicMinorScale(),
          "ascending_melodic_minor": AscendingMelodicMinorScale()
     }

     def __init__(self, note_letter, alteration, scale):
          self.tonic = PitchClassSpelling(note_letter, alteration)
          if not scale in Key.scale_mapping:
               raise KeyError("scale '{}' is not supported.".format(scale))
          self.mode = Key.scale_mapping[scale]
          self.i = self.I = self.scale_degree(1)
          self.ii = self.II = self.scale_degree(2)
          self.iii = self.III = self.scale_degree(3)
          self.iv = self.IV = self.scale_degree(4)
          self.v = self.V = self.scale_degree(5)
          self.vi = self.VI = self.scale_degree(6)
          self.vii = self.VII = self.scale_degree(7)

     def scale_degree(self, scale_degree):
          if 1 > scale_degree and scale_degree > DIATONIC_CLASSES:
               raise ValueError("scale degree should be within 1 and 7.")
          interval = self.mode.step_to_interval_spelling(scale_degree)
          return self.tonic.to_interval(interval)


class Harmalysis(object):
     def __init__(self):
          self.reference_key = None
          self.established_key = None
          self.chord = None


class ChordBase(object):
     def __init__(self):
          self.root = None
          self._intervals = [None] * 14
          self.bass = None
          self.second = self._intervals[0]
          self.third = self._intervals[1]
          self.fourth = self._intervals[2]
          self.fifth = self._intervals[3]
          self.sixth = self._intervals[4]
          self.seventh = self._intervals[5]
          self.ninth = self._intervals[7]
          self.tenth = self._intervals[8]
          self.eleventh = self._intervals[9]
          self.twelfth = self._intervals[10]
          self.thirteenth = self._intervals[11]
          self.fourteenth = self._intervals[12]
          self.fifteenth = self._intervals[13]

     def added_interval(self, general_interval):
          return self._intervals[general_interval - 2]

     def __str__(self):
          ret = str(self.root)
          for interval in self._intervals:
               if interval:
                    ret += str(interval)


class TertianChord(ChordBase):
     def __init__(self, missing_intervals=[]):
          super().__init__()
          self.scale_degree = None
          self.triad_quality = None
          self.inversion = None
          self.default_function = None
          self.contextual_function = None
          self.chord_label = None
          self.pcset = None


@v_args(inline=True)
class HarmalysisParser(Transformer):
     ##################
     ## Parsing the key
     ##################

     # Key scales

     # # Verbose version
     # def major_key(self, letter):
     #      print(sys._getframe().f_code.co_name, letter)
     #      key_definition = Key(letter, None, 'major')
     #      return key_definition

     major_key = lambda self, letter: Key(letter, None, 'major')
     major_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'major')
     default_minor_key = lambda self, letter: Key(letter, None, 'default_minor')
     default_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'default_minor')
     natural_minor_key = lambda self, letter: Key(letter, None, 'natural_minor')
     natural_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'natural_minor')
     harmonic_minor_key = lambda self, letter: Key(letter, None, 'harmonic_minor')
     harmonic_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'harmonic_minor')
     melodic_minor_key = lambda self, letter: Key(letter, None, 'ascending_melodic_minor')
     melodic_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'ascending_melodic_minor')

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
     augmented_triad = lambda self, scale_degree: ('augmented_triad', str(scale_degree), None)
     augmented_triad_with_alteration = lambda self, alteration, scale_degree: ('augmented_triad', str(scale_degree), str(alteration))
     diminished_triad = lambda self, scale_degree: ('diminished_triad', str(scale_degree), None)
     diminished_triad_with_alteration = lambda self, alteration, scale_degree: ('diminished_triad', str(scale_degree), str(alteration))

     # Missing intervals
     missing_intervals_triad = list
     missing_intervals_seventhchord = list
     missing_intervals_ninthchord = list
     missing_intervals_eleventhchord = list
     missing_intervals_thirteenthchord = list

     #############################
     ## Parsing a harmalysis entry
     #############################
     def harmalysis_tertian(self, tertian):
          print(sys._getframe().f_code.co_name, tertian)

     def harmalysis_tertian_with_key(self, key, tertian):
          print(sys._getframe().f_code.co_name, key, tertian)

     def harmalysis_tertian_with_tonicization(self, tertian, tonicization):
          print(sys._getframe().f_code.co_name, tertian, tonicization)

     def harmalysis_tertian_with_key_and_tonicization(self, key, tertian, tonicization):
          print(sys._getframe().f_code.co_name, key, tertian, tonicization)

test_strings = [
     'C:viio65',
     'f#_nat:#viiom7b|f#_nat:vii065|?e#m3D5m7',
     'f#_nat:#viiom7bx5[f#_nat=>:vii065]',
]

def test_intervals():
     orig = PitchClassSpelling('C')
     M6 = IntervalSpelling('P', 1)
     target = orig.to_interval(M6)
     print(target)

def test_key():
     note_letter, alteration, scale = 'f', None, 'major'
     key = Key(note_letter, alteration, scale)
     print(key.i, key.II, key.iii, key.IV, key.V, key.vi, key.VII)

if __name__ == '__main__':
     grammar = 'harmalysis.lark'
     l = Lark(open(grammar).read(), start="start")
     t = l.parse(sys.argv[1])
     print(t)
     print(t.pretty())
     tree.pydot__tree_to_png(t, 'harmparser.png')
     print("Transformer")
     HarmalysisParser().transform(t)


