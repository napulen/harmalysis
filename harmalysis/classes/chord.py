'''
    harmalysis - a language for harmonic analysis and roman numerals
    Copyright (C) 2020  Nestor Napoles Lopez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from harmalysis.classes import interval

class DescriptiveChord(object):
     def __init__(self):
          self.scale_degree = None
          self.scale_degree_alteration = None
          self.root = None
          self.intervals = {interval: None for interval in range(2,16)}
          self.bass = None
          self.default_function = None
          self.contextual_function = None
          self.chord_label = None
          self.pcset = None

     def add_interval(self, interval_spelling):
          if not isinstance(interval_spelling, interval.IntervalSpelling):
               raise TypeError('expected type IntervalSpelling instead of {}'.format(type(interval_spelling)))
          if interval_spelling.diatonic_interval not in self.intervals:
               raise ValueError('interval {} is out of bounds'.format(interval_spelling.diatonic_interval))
          self.intervals[interval_spelling.diatonic_interval] = interval_spelling

     def missing_interval(self, diatonic_interval):
          if diatonic_interval not in self.intervals:
               raise ValueError('interval {} is out of bounds'.format(diatonic_interval))
          self.intervals[diatonic_interval] = None

     def __str__(self):
          ret = str(self.root)
          for interval in self.intervals.values():
               if interval:
                    ret += str(interval)
          return ret


class InvertibleChord(DescriptiveChord):
     inversions_by_number = [
          6, 64, 65, 43, 42, 2
     ]
     inversions_by_letter = [
          'a', 'b', 'c', 'd', 'e', 'f', 'g'
     ]
     def __init__(self):
          super().__init__()
          self.inversion = 0

     def set_inversion_by_number(self, inversion_by_number):
          if not inversion_by_number in self.inversions_by_number:
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
          if not inversion_by_letter in self.inversions_by_letter:
               raise KeyError("the inversion letter '{}' is not supported".format(inversion_by_letter))
          self.inversion = self.inversions_by_letter.index(inversion_by_letter)


class TertianChord(InvertibleChord):
     triad_qualities = [
          'major_triad',
          'minor_triad',
          'diminished_triad',
          'augmented_triad'
     ]
     def __init__(self):
          super().__init__()
          self.triad_quality = None

     def set_triad_quality(self, triad_quality):
          if not triad_quality in TertianChord.triad_qualities:
               raise KeyError("the triad quality '{}' is not supported".format(triad_quality))
          self.triad_quality = triad_quality
          if triad_quality == 'major_triad':
               self.add_interval(interval.IntervalSpelling('M', 3))
               self.add_interval(interval.IntervalSpelling('P', 5))
          elif triad_quality == 'minor_triad':
               self.add_interval(interval.IntervalSpelling('m', 3))
               self.add_interval(interval.IntervalSpelling('P', 5))
          elif triad_quality == 'diminished_triad':
               self.add_interval(interval.IntervalSpelling('m', 3))
               self.add_interval(interval.IntervalSpelling('D', 5))
          elif triad_quality == 'augmented_triad':
               self.add_interval(interval.IntervalSpelling('M', 3))
               self.add_interval(interval.IntervalSpelling('A', 5))

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


class AugmentedSixthChord(InvertibleChord):
     def __init__(self, augmented_sixth_type):
          super().__init__()
          self.scale_degree = "iv"
          self.scale_degree_alteration = '#'
          self.add_interval(interval.IntervalSpelling("D", 3))
          self.add_interval(interval.IntervalSpelling("D", 5))
          self.augmented_sixth_type = augmented_sixth_type
          if self.augmented_sixth_type == 'german':
               self.add_interval(interval.IntervalSpelling("D", 7))
          elif self.augmented_sixth_type == 'french':
               self.add_interval(interval.IntervalSpelling("m", 6))


class NeapolitanChord(TertianChord):
     def __init__(self):
          super().__init__()
          self.scale_degree = "II"
          self.scale_degree_alteration = "b"
          self.triad_quality = "major_triad"
          self.add_interval(interval.IntervalSpelling('M', 3))
          self.add_interval(interval.IntervalSpelling('P', 5))


class HalfDiminishedChord(TertianChord):
     def __init__(self):
          super().__init__()
          self.scale_degree = "vii"
          # TODO: Figure out the alteration (vii or #vii; will be complicated)
          self.triad_quality = "diminished_triad"
          self.add_interval(interval.IntervalSpelling("m", 3))
          self.add_interval(interval.IntervalSpelling("D", 5))
          self.add_interval(interval.IntervalSpelling("m", 7))


class CadentialSixFourChord(TertianChord):
     def __init__(self):
          super().__init__()
          self.set_inversion_by_number(64)

     def set_as_major(self):
          self.scale_degree = "I" # or V, HUGE dilemma
          self.triad_quality = "major_triad"
          self.add_interval(interval.IntervalSpelling("M", 3))
          self.add_interval(interval.IntervalSpelling("P", 5))

     def set_as_minor(self):
          self.scale_degree = "i"
          self.triad_quality = "minor_triad"
          self.add_interval(interval.IntervalSpelling("m", 3))
          self.add_interval(interval.IntervalSpelling("P", 5))


class CommonToneDiminishedChord(TertianChord):
     def __init__(self):
          super().__init__()
          self.scale_degree = "I"
          self.triad_quality = "diminished_triad"
          self.add_interval(interval.IntervalSpelling("m", 3))
          self.add_interval(interval.IntervalSpelling("D", 5))
          self.add_interval(interval.IntervalSpelling("D", 7))

