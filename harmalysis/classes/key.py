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

from harmalysis.classes import scale, interval, pitch_class
import harmalysis.common as common


class Key(object):
    _scale_mapping = {
        "major": scale.MajorScale(),
        "natural_minor": scale.NaturalMinorScale(),
        "harmonic_minor": scale.HarmonicMinorScale(), "minor": scale.HarmonicMinorScale(),
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