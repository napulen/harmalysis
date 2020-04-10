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
        if not note_letter in self.diatonic_classes:
            raise ValueError("note letter '{}' is not supported.".format(note_letter))
        self.note_letter = note_letter
        self.diatonic_class = self.diatonic_classes.index(note_letter)
        if alteration:
            if not alteration in self.alterations:
                raise ValueError("alteration '{}' is not supported.".format(alteration))
            self.alteration = alteration
            alteration_value = self.alterations[alteration]
        else:
            self.alteration = ''
            alteration_value = 0
        default_chromatic_class = self.pitch_classes[self.diatonic_class]
        self.chromatic_class = (12 + default_chromatic_class + alteration_value) % 12

    @classmethod
    def from_diatonic_chromatic_classes(cls, diatonic_class, chromatic_class):
        if  0 > diatonic_class or diatonic_class >= harmalysis.common.DIATONIC_CLASSES:
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

        new_diatonic_class = (diatonic_steps + self.diatonic_class) % harmalysis.common.DIATONIC_CLASSES
        new_chromatic_class = (semitones + self.chromatic_class) % 12
        return PitchClassSpelling.from_diatonic_chromatic_classes(new_diatonic_class, new_chromatic_class)

    def __str__(self):
        return '{}{}'.format(self.note_letter, self.alteration)

