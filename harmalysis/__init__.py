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

def parse(query, syntax='roman'):
    if syntax == 'roman':
        roman = harmalysis.parsers.roman.parse(query)
        return roman
    elif syntax == 'chordlabel':
        chordlabel = harmalysis.parsers.chordlabel.parse(query)
        return chordlabel