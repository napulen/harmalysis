'''
The harmalysis language for harmonic analysis and roman numerals

Copyright (c) 2019, Néstor Nápoles
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

from lark import Lark, tree, Transformer, v_args
import sys


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


grammarfile = 'harmalysis_chordlabel.lark'
parser = Lark(open(grammarfile).read())
pngs_folder = 'ast_pngs/'

def parse(query, full_tree=False, create_png=True):
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