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

import harmalysis.parsers.roman
import harmalysis.parsers.chordlabel
import harmalysis.classes.pitch_class
import lark.exceptions
import sys

test_strings = [
    'C:viio65',
    'f#_nat:#viiom7b|f#_nat:vii065|?e#m3D5m7',
    'f#_nat:#viiom7bx5[f#_nat=>:vii065]',
]

if __name__ == '__main__':
    while True:
        try:
            query = input('> ')
        except EOFError:
            break
        try:
            roman = harmalysis.parsers.roman.parse(query)
            chordlabel = harmalysis.parsers.chordlabel.parse(str(roman.chord))
        except lark.exceptions.UnexpectedCharacters:
            print('Invalid entry. Try again.')
            continue
        print('\tMain key: ' + str(roman.main_key))
        print('\tSecondary key: ' + str(roman.secondary_key))
        print('\tIntervallic construction: ' + str(roman.chord))
        print('\tInversion: ' + str(roman.chord.inversion))
        print('\tChord label: ' + chordlabel)
        print('\tDefault function: ' + roman.chord.default_function)
        print('\tContextual function: ' + roman.chord.contextual_function)


