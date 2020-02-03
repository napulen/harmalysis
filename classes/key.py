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

from harmalysis.classes import scale, interval, pitch_class
import harmalysis.common as common

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
          self.tonic = pitch_class.PitchClassSpelling(note_letter, alteration)
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