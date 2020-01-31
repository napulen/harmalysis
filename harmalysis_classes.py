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

import common
import interval
import scale
import equal_temperament

class Key(object):
     _scale_mapping = {
          "major": scale.MajorScale(),
          "natural_minor": scale.NaturalMinorScale(),
          "harmonic_minor": scale.HarmonicMinorScale(), "default_minor": scale.HarmonicMinorScale(),
          "ascending_melodic_minor": scale.AscendingMelodicMinorScale()
     }
     _scale_degree_alterations = {
          '--': interval.IntervalSpelling('DD', 1),
          'bb': interval.IntervalSpelling('DD', 1),
          '-': interval.IntervalSpelling('D', 1),
          'b': interval.IntervalSpelling('D', 1),
          "#": interval.IntervalSpelling('A', 1),
          "##": interval.IntervalSpelling('AA', 1),
          "x": interval.IntervalSpelling('AA', 1)
     }

     def __init__(self, note_letter, alteration=None, scale="major"):
          self.tonic = equal_temperament.PitchClassSpelling(note_letter, alteration)
          self.scale = scale
          if not scale in self._scale_mapping:
               raise KeyError("scale '{}' is not supported.".format(scale))
          self.mode = Key._scale_mapping[scale]

     def scale_degree(self, scale_degree, alteration=None):
          if type(scale_degree) == str:
               if scale_degree not in common.roman_to_int:
                    raise ValueError("scale degree {} is not supported.".format(scale_degree))
               scale_degree = common.roman_to_int[scale_degree]
          if 1 > scale_degree or scale_degree > common.DIATONIC_CLASSES:
               raise ValueError("scale degree should be within 1 and 7.")
          interval = self.mode.step_to_interval_spelling(scale_degree)
          pc = self.tonic.to_interval(interval)
          if alteration:
               if not alteration in self._scale_degree_alterations:
                    raise KeyError("alteration '{}' is not supported.".format(alteration))
               unison_alteration = self._scale_degree_alterations[alteration]
               pc = pc.to_interval(unison_alteration)
          return pc

     def __str__(self):
          return str(self.tonic) + " " + self.scale


class Harmalysis(object):
     established_key = Key("C", scale="major")
     def __init__(self):
          self.reference_key = None
          self.applied_key = None
          self.chord = None
          self.tonicized_keys = []

def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


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
          self.scale_degree = "I" # or V, HUGE dilemma
          self.triad_quality = "major_triad"
          self.add_interval(interval.IntervalSpelling("M", 3))
          self.add_interval(interval.IntervalSpelling("P", 5))
          self.set_inversion_by_number(64)


class CommonToneDiminishedChord(TertianChord):
     def __init__(self):
          super().__init__()
          self.scale_degree = "I"
          self.triad_quality = "diminished_triad"
          self.add_interval(interval.IntervalSpelling("m", 3))
          self.add_interval(interval.IntervalSpelling("D", 5))
          self.add_interval(interval.IntervalSpelling("D", 7))

