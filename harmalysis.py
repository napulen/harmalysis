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

roman_to_int = {
     'I':   1, 'i':   1,
     'II':  2, 'ii':  2,
     'III': 3, 'iii': 3,
     'IV':  4, 'iv':  4,
     'V':   5, 'v':   5,
     'VI':  6, 'vi':  6,
     'VII': 7, 'vii': 7
}

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
          self.qualities = [
               # Starting from I
               ['P', 'M', 'M', 'P', 'P', 'M', 'M'],
               # Starting from II
               ['P', 'M', 'm', 'P', 'P', 'M', 'm'],
               # Starting from III
               ['P', 'm', 'm', 'P', 'P', 'm', 'm'],
               # Starting from IV
               ['P', 'M', 'M', 'A', 'P', 'M', 'M'],
               # Starting from V
               ['P', 'M', 'M', 'P', 'P', 'M', 'm'],
               # Starting from VI
               ['P', 'M', 'm', 'P', 'P', 'm', 'm'],
               # Starting from VII
               ['P', 'm', 'm', 'P', 'D', 'm', 'm'],
          ]

          self.semitones = [
               # Starting from I
               [0, 2, 4, 5, 7, 9, 11],
               # Starting from II
               [0, 2, 3, 5, 7, 9, 10],
               # Starting from III
               [0, 1, 3, 5, 7, 8, 10],
               # Starting from IV
               [0, 2, 4, 6, 7, 9, 11],
               # Starting from V
               [0, 2, 4, 5, 7, 9, 10],
               # Starting from VI
               [0, 2, 3, 5, 7, 8, 10],
               # Starting from VII
               [0, 1, 3, 5, 6, 8, 10],
          ]

     def step_to_interval_spelling(self, step, mode=1):
          qualities = self.qualities[(mode - 1) % DIATONIC_CLASSES]
          quality = qualities[(step - 1) % DIATONIC_CLASSES]
          return IntervalSpelling(quality, step)

     def step_to_semitones(self, step, mode=1):
          semitones = self.semitones[(mode - 1) % DIATONIC_CLASSES]
          step_semitones = semitones[(step - 1) % DIATONIC_CLASSES]
          octaves = (step - 1) // DIATONIC_CLASSES
          self.semitones = (12 * octaves) + step_semitones
          return self.semitones


class NaturalMinorScale(MajorScale):
     def __init__(self):
          super().__init__()
          self.qualities = [
               ['P', 'M', 'm', 'P', 'P', 'm', 'm'],
               ['P', 'm', 'm', 'P', 'D', 'm', 'm'],
               ['P', 'M', 'M', 'P', 'P', 'M', 'M'],
               ['P', 'M', 'm', 'P', 'P', 'M', 'm'],
               ['P', 'm', 'm', 'P', 'P', 'm', 'm'],
               ['P', 'M', 'M', 'A', 'P', 'M', 'M'],
               ['P', 'M', 'M', 'P', 'P', 'M', 'm'],
          ]

          self.semitones = [
               [0, 2, 3, 5, 7, 8, 10],
               [0, 1, 3, 5, 6, 8, 10],
               [0, 2, 4, 5, 7, 9, 11],
               [0, 2, 3, 5, 7, 9, 10],
               [0, 1, 3, 5, 7, 8, 10],
               [0, 2, 4, 6, 7, 9, 11],
               [0, 2, 4, 5, 7, 9, 10],
          ]


class HarmonicMinorScale(NaturalMinorScale):
     def __init__(self):
          super().__init__()
          self.qualities = [
               ['P', 'M', 'm', 'P', 'P', 'm', 'M'],
               ['P', 'm', 'm', 'P', 'D', 'M', 'm'],
               ['P', 'M', 'M', 'P', 'A', 'M', 'M'],
               ['P', 'M', 'm', 'A', 'P', 'M', 'm'],
               ['P', 'm', 'M', 'P', 'P', 'm', 'm'],
               ['P', 'A', 'M', 'A', 'P', 'M', 'M'],
               ['P', 'm', 'm', 'D', 'D', 'm', 'D'],
          ]

          self.semitones = [
               [0, 2, 3, 5, 7, 8, 11],
               [0, 1, 3, 5, 6, 9, 10],
               [0, 2, 4, 5, 6, 9, 11],
               [0, 2, 3, 6, 7, 9, 10],
               [0, 1, 4, 5, 7, 8, 10],
               [0, 3, 4, 6, 7, 9, 11],
               [0, 1, 3, 4, 6, 8, 9],
          ]


class AscendingMelodicMinorScale(HarmonicMinorScale):
     def __init__(self):
          super().__init__()
          self.qualities = [
               ['P', 'M', 'm' , 'P', 'P', 'M', 'M'],
               ['P', 'm', 'm' , 'P', 'P', 'M', 'm'],
               ['P', 'M', 'M' , 'A', 'A', 'M', 'M'],
               ['P', 'M', 'M' , 'A', 'P', 'M', 'm'],
               ['P', 'M', 'M' , 'P', 'P', 'm', 'm'],
               ['P', 'M', 'm' , 'P', 'D', 'm', 'm'],
               ['P', 'm', 'm' , 'D', 'D', 'm', 'm'],
          ]

          self.semitones = [
               [0, 2, 3, 5, 7, 9, 11],
               [0, 1, 3, 5, 7, 9, 10],
               [0, 2, 4, 6, 8, 9, 11],
               [0, 2, 4, 6, 7, 9, 10],
               [0, 2, 4, 5, 7, 8, 10],
               [0, 2, 3, 5, 6, 8, 10],
               [0, 1, 3, 4, 6, 8, 10]
          ]


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
          if 1 > scale_degree or scale_degree > DIATONIC_CLASSES:
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

     def add_interval(self, interval_spelling):
          if not isinstance(interval_spelling, IntervalSpelling):
               raise TypeError('expected type IntervalSpelling instead of {}'.format(type(interval_spelling)))
          self._intervals[interval_spelling.diatonic_interval - 2] = interval_spelling

     def missing_interval(self, diatonic_interval):
          self._intervals[diatonic_interval - 2] = None

     def __str__(self):
          ret = str(self.root)
          for interval in self._intervals:
               if interval:
                    ret += str(interval)
          return ret


class TertianChord(ChordBase):
     triad_qualities = [
          'major_triad',
          'minor_triad',
          'diminished_triad',
          'augmented_triad'
     ]
     inversions_by_number = [
          6, 64, 65, 43, 42, 2
     ]
     inversions_by_letter = [
          'a', 'b', 'c', 'd', 'e', 'f', 'g'
     ]
     def __init__(self):
          super().__init__()
          self.scale_degree = None
          self.scale_degree_alteration = None
          self.triad_quality = None
          self.inversion = None
          self.default_function = None
          self.contextual_function = None
          self.chord_label = None
          self.pcset = None

     def set_triad_quality(self, triad_quality):
          if not triad_quality in TertianChord.triad_qualities:
               raise KeyError("the triad quality '{}' is not supported".format(triad_quality))
          self.triad_quality = triad_quality
          if triad_quality == 'major_triad':
               self.add_interval(IntervalSpelling('M', 3))
               self.add_interval(IntervalSpelling('P', 5))
          elif triad_quality == 'minor_triad':
               self.add_interval(IntervalSpelling('m', 3))
               self.add_interval(IntervalSpelling('P', 5))
          elif triad_quality == 'diminished_triad':
               self.add_interval(IntervalSpelling('m', 3))
               self.add_interval(IntervalSpelling('D', 5))
          elif triad_quality == 'augmented_triad':
               self.add_interval(IntervalSpelling('M', 3))
               self.add_interval(IntervalSpelling('A', 5))

     def set_inversion_by_number(self, inversion_by_number):
          if not inversion_by_number in TertianChord.inversions_by_number:
               raise KeyError("the numeric inversion '{}' is not supported".format(inversion_by_number))
          if inversion_by_number == 6:
               self.inversion = 1
          elif inversion_by_number == 64:
               self.inversion = 2
          elif inversion_by_number == 65:
               self.inversion = 1
          elif inversion_by_number == 43:
               self.inversion = 2
          elif inversion_by_number == 42 or inversion_by_number == 2:
               self.inversion = 3

     def set_inversion_by_letter(self, inversion_by_letter):
          if not inversion_by_letter in TertianChord.inversions_by_letter:
               raise KeyError("the inversion letter '{}' is not supported".format(inversion_by_letter))
          self.inversion = TertianChord.inversions_by_letter.index(inversion_by_letter)

     # def __str__(self):
     #      ret = """
     #      scale degree: {}
     #      triad quality: {}
     #      inversion: {}
     #      intervals: {}
     #      """.format(self.scale_degree,
     #      self.triad_quality,
     #      self.inversion,
     #      self._intervals)
     #      return ret

def _tertian_chord(triad, missing_intervals, inversion_by_number=None, inversion_by_letter=None, added_interval=None):
     tertian = TertianChord()
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
          if isinstance(added_interval, IntervalSpelling):
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

     for interval in missing_intervals:
          tertian.missing_interval(int(interval))
     
     return (tertian, diatonic_intervals)

def _harmalysis():
     '''hi'''


@v_args(inline=True)
class HarmalysisParser(Transformer):
     ##################
     ## Parsing the key
     ##################
     # Key scales
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
     augmented_triad = lambda self, scale_degree, _: ('augmented_triad', str(scale_degree), None)
     augmented_triad_with_alteration = lambda self, alteration, scale_degree, _: ('augmented_triad', str(scale_degree), str(alteration))
     diminished_triad = lambda self, scale_degree, _: ('diminished_triad', str(scale_degree), None)
     diminished_triad_with_alteration = lambda self, alteration, scale_degree, _: ('diminished_triad', str(scale_degree), str(alteration))
     # Inversions by number
     triad_inversion_by_number = lambda self, inversion: int(inversion)
     seventhchord_inversion_by_number = lambda self, inversion: int(inversion)
     # Inversions by letter
     inversion_by_letter = lambda self, inversion: str(inversion)
     # Added intervals
     added_seventh_diatonic = lambda self, interval: int(interval)
     added_seventh_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
     added_ninth_diatonic = lambda self, interval: int(interval)
     added_ninth_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
     added_eleventh_diatonic = lambda self, interval: int(interval)
     added_eleventh_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
     added_thirteenth_diatonic = lambda self, interval: int(interval)
     added_thirteenth_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
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
          print(sys._getframe().f_code.co_name, tertian)

     def harmalysis_tertian_with_key(self, key, tertian):
          print(sys._getframe().f_code.co_name, key, tertian)
          harmalysis = Harmalysis()
          key, function = key
          if function == 'reference':
               harmalysis.reference_key = key
          elif function == 'established':
               harmalysis.established_key = key
          tertian_chord, diatonic_intervals = tertian
          scale_degree = tertian_chord.scale_degree
          root_diatonic_step = roman_to_int[scale_degree]
          tertian_chord.root = getattr(key, scale_degree)
          for diatonic in diatonic_intervals:
               interval = key.mode.step_to_interval_spelling(diatonic, mode=root_diatonic_step)
               tertian_chord.add_interval(interval)
          harmalysis.chord = tertian_chord
          return harmalysis

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
     x = HarmalysisParser().transform(t)
     print(str(x.chord))


