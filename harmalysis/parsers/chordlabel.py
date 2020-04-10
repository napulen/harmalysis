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

from lark import Lark, tree, Transformer, v_args
import sys
import pathlib
import os


@v_args(inline=True)
class ChordLabelParser(Transformer):
    root = str
    root_with_alteration = lambda self, letter, alteration: "{}{}".format(letter, alteration)
    major_triad_chord = lambda self: 'major'
    minor_triad_chord = lambda self: 'minor'
    augmented_triad_chord = lambda self: 'augmented'
    diminished_triad_chord = lambda self: 'diminished'
    major_seventh_chord = lambda self: 'major seventh'
    dominant_seventh_chord = lambda self: 'dominant seventh'
    augmented_major_seventh_chord = lambda self: 'augmented major seventh'
    minor_seventh_chord = lambda self: 'minor seventh'
    minor_major_seventh_chord = lambda self: 'minor major seventh'
    half_diminished_seventh_chord = lambda self: 'half-diminished seventh'
    fully_diminished_seventh_chord = lambda self: 'fully-diminished seventh'
    italian_augmented_sixth = lambda self: 'italian augmented sixth'
    french_augmented_sixth = lambda self: 'french augmented sixth'
    german_augmented_sixth = lambda self: 'german augmented sixth'
    chordlabel = lambda self, root, chord: "{} {}".format(root, chord)


current_dir = pathlib.Path(__file__).parent.absolute()
grammarfile = os.path.join(str(current_dir), 'chordlabel.lark')
parser = Lark(open(grammarfile).read())
pngs_folder = os.path.join(str(current_dir), 'ast_pngs/')

def parse(query, full_tree=False, create_png=False):
    ast = parser.parse(query)
    if create_png:
        tree.pydot__tree_to_png(ast, '{}{}.png'.format(pngs_folder, query))
    if full_tree:
        return ast
    return ChordLabelParser().transform(ast)

if __name__ == '__main__':
    ast = parse(sys.argv[1], full_tree=True)
    print(ChordLabelParser().transform(ast))
    tree.pydot__tree_to_png(ast, 'ast_pngs/harmalysis_chordlabel.png')