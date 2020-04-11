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

import harmalysis.common
from harmalysis.classes import pitch_class
from harmalysis.classes import scale


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
        diatonic_classes_with_perfect_intervals = [harmalysis.common.TONIC, harmalysis.common.SUBDOMINANT, harmalysis.common.DOMINANT]
        diatonic_class = (diatonic_interval - 1) % harmalysis.common.DIATONIC_CLASSES
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
    orig = pitch_class.PitchClassSpelling('C')
    M6 = IntervalSpelling('P', 1)
    target = orig.to_interval(M6)
    print(target)