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
          if  0 > diatonic_class or diatonic_class >= common.DIATONIC_CLASSES:
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
          if not isinstance(interval_spelling, interval.IntervalSpelling):
               raise TypeError('expecting IntervalSpelling instead of {}.'.format(type(interval_spelling)))
          diatonic_steps = interval_spelling.diatonic_interval - 1
          semitones = interval_spelling.semitones

          new_diatonic_class = (diatonic_steps + self.diatonic_class) % common.DIATONIC_CLASSES
          new_chromatic_class = (semitones + self.chromatic_class) % 12
          return PitchClassSpelling.from_diatonic_chromatic_classes(new_diatonic_class, new_chromatic_class)

     def __str__(self):
          return '{}{}'.format(self.note_letter, self.alteration)

