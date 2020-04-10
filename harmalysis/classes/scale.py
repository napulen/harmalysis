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
from harmalysis.classes import interval

class MajorScale(object):
    def __init__(self):
        self._qualities = [
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

        self._semitones = [
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
        qualities = self._qualities[(mode - 1) % harmalysis.common.DIATONIC_CLASSES]
        quality = qualities[(step - 1) % harmalysis.common.DIATONIC_CLASSES]
        return interval.IntervalSpelling(quality, step)

    def step_to_semitones(self, step, mode=1):
        semitones = self._semitones[(mode - 1) % harmalysis.common.DIATONIC_CLASSES]
        step_semitones = semitones[(step - 1) % harmalysis.common.DIATONIC_CLASSES]
        octaves = (step - 1) // harmalysis.common.DIATONIC_CLASSES
        distance = (12 * octaves) + step_semitones
        return distance


class NaturalMinorScale(MajorScale):
    def __init__(self):
        super().__init__()
        self._qualities = [
            ['P', 'M', 'm', 'P', 'P', 'm', 'm'],
            ['P', 'm', 'm', 'P', 'D', 'm', 'm'],
            ['P', 'M', 'M', 'P', 'P', 'M', 'M'],
            ['P', 'M', 'm', 'P', 'P', 'M', 'm'],
            ['P', 'm', 'm', 'P', 'P', 'm', 'm'],
            ['P', 'M', 'M', 'A', 'P', 'M', 'M'],
            ['P', 'M', 'M', 'P', 'P', 'M', 'm'],
        ]

        self._semitones = [
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
        self._qualities = [
            ['P', 'M', 'm', 'P', 'P', 'm', 'M'],
            ['P', 'm', 'm', 'P', 'D', 'M', 'm'],
            ['P', 'M', 'M', 'P', 'A', 'M', 'M'],
            ['P', 'M', 'm', 'A', 'P', 'M', 'm'],
            ['P', 'm', 'M', 'P', 'P', 'm', 'm'],
            ['P', 'A', 'M', 'A', 'P', 'M', 'M'],
            ['P', 'm', 'm', 'D', 'D', 'm', 'D'],
        ]

        self._semitones = [
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
        self._qualities = [
            ['P', 'M', 'm', 'P', 'P', 'M', 'M'],
            ['P', 'm', 'm', 'P', 'P', 'M', 'm'],
            ['P', 'M', 'M', 'A', 'A', 'M', 'M'],
            ['P', 'M', 'M', 'A', 'P', 'M', 'm'],
            ['P', 'M', 'M', 'P', 'P', 'm', 'm'],
            ['P', 'M', 'm', 'P', 'D', 'm', 'm'],
            ['P', 'm', 'm', 'D', 'D', 'm', 'm'],
        ]

        self._semitones = [
            [0, 2, 3, 5, 7, 9, 11],
            [0, 1, 3, 5, 7, 9, 10],
            [0, 2, 4, 6, 8, 9, 11],
            [0, 2, 4, 6, 7, 9, 10],
            [0, 2, 4, 5, 7, 8, 10],
            [0, 2, 3, 5, 6, 8, 10],
            [0, 1, 3, 4, 6, 8, 10]
        ]