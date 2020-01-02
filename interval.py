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
import equal_temperament
import interval
import scale

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
          diatonic_classes_with_perfect_intervals = [common.TONIC, common.SUBDOMINANT, common.DOMINANT]
          diatonic_class = (diatonic_interval - 1) % common.DIATONIC_CLASSES
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
          self.semitones = scale.MajorScale().step_to_semitones(diatonic_interval) + self.alteration_effect

     def __str__(self):
          return '{}{}'.format(self.interval_quality, self.diatonic_interval)


def test_intervals():
     orig = equal_temperament.PitchClassSpelling('C')
     M6 = IntervalSpelling('P', 1)
     target = orig.to_interval(M6)
     print(target)