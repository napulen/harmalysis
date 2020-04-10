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

TONIC = 0
SUPERTONIC = 1
MEDIANT = 2
SUBDOMINANT = 3
DOMINANT = 4
SUBMEDIANT = 5
SEVENTH_DEGREE = 6
DIATONIC_CLASSES = 7

# Lighter than loading an entire module just for this
roman_to_int = {
    'I':   1, 'i':   1,
    'II':  2, 'ii':  2,
    'III': 3, 'iii': 3,
    'IV':  4, 'iv':  4,
    'V':   5, 'v':   5,
    'VI':  6, 'vi':  6,
    'VII': 7, 'vii': 7
}