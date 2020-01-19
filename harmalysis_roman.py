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
import common
import interval
import harmalysis_classes
import sys

def _tertian_chord(triad, missing_intervals, inversion_by_number=None, inversion_by_letter=None, added_interval=None):
     tertian = harmalysis_classes.TertianChord()
     triad_quality, scale_degree, alteration = triad
     tertian.scale_degree = scale_degree
     tertian.scale_degree_alteration = alteration
     tertian.set_triad_quality(triad_quality)
     # Handling inversions
     if inversion_by_number:
          tertian.set_inversion_by_number(inversion_by_number)
     elif inversion_by_letter:
          tertian.set_inversion_by_letter(inversion_by_letter)
     # Handling added intervals
     diatonic_intervals = []
     if added_interval:
          if isinstance(added_interval, interval.IntervalSpelling):
               tertian.add_interval(added_interval)
          else:
               if added_interval == 7:
                    diatonic_intervals = [7]
               elif added_interval == 9:
                    diatonic_intervals = [7, 9]
               elif added_interval == 11:
                    diatonic_intervals = [7, 9, 11]
               elif added_interval == 13:
                    diatonic_intervals = [7, 9, 11, 13]
     # Handling missing intervals
     for i in missing_intervals:
          tertian.missing_interval(int(i))
     return (tertian, diatonic_intervals)

def _special_chord(name, inversion_by_number=None, inversion_by_letter=None):
     if name == "Gn" or name == "Ger":
          special = harmalysis_classes.AugmentedSixthChord('german')
     elif name == 'Fr':
          special = harmalysis_classes.AugmentedSixthChord('french')
     elif name == 'It' or name == "Lt":
          special = harmalysis_classes.AugmentedSixthChord('italian')
     elif name == "N":
          special = harmalysis_classes.NeapolitanChord()
     elif name == "Cad" or name == "Cad64":
          special = harmalysis_classes.CadentialSixFourChord()
     elif name == "CTo" or name == "CTo7":
          special = harmalysis_classes.CommonToneDiminishedChord()
     # Handling inversions
     if inversion_by_number:
          special.set_inversion_by_number(inversion_by_number)
     elif inversion_by_letter:
          special.set_inversion_by_letter(inversion_by_letter)
     return special

def _harmalysis_tertian(tertian, key_function=None, tonicizations=[]):
     harmalysis = harmalysis_classes.Harmalysis()
     if key_function:
          key, function = key_function
          if function == 'reference':
               harmalysis.reference_key = key
          elif function == 'established':
               harmalysis_classes.Harmalysis.established_key = key
     else:
          key = harmalysis_classes.Harmalysis.established_key
     current_key = key
     tonicized_keys = []
     for tonicization in reversed(tonicizations):
          alteration, degree, mode = tonicization
          tonicized_pc = current_key.scale_degree(common.roman_to_int[degree], alteration)
          tonicized_key = harmalysis_classes.Key(tonicized_pc.note_letter, tonicized_pc.alteration, mode)
          tonicized_keys.insert(0, tonicized_key)
          current_key = tonicized_key
     tertian_chord, diatonic_intervals = tertian
     degree = tertian_chord.scale_degree
     degree_alteration = tertian_chord.scale_degree_alteration
     root_diatonic_step = common.roman_to_int[degree]
     tertian_chord.root = current_key.scale_degree(common.roman_to_int[degree], degree_alteration)
     for diatonic in diatonic_intervals:
          interval = current_key.mode.step_to_interval_spelling(diatonic, mode=root_diatonic_step)
          tertian_chord.add_interval(interval)
     harmalysis.chord = tertian_chord
     return harmalysis


def _harmalysis_special(special, key_function=None, tonicizations=[]):
     harmalysis = harmalysis_classes.Harmalysis()
     if key_function:
          key, function = key_function
          if function == 'reference':
               harmalysis.reference_key = key
          elif function == 'established':
               harmalysis.established_key = key
     else:
          key = harmalysis_classes.Harmalysis.established_key
     current_key = key
     tonicized_keys = []
     for tonicization in reversed(tonicizations):
          alteration, degree, mode = tonicization
          tonicized_pc = current_key.scale_degree(common.roman_to_int[degree], alteration)
          tonicized_key = harmalysis_classes.Key(tonicized_pc.note_letter, tonicized_pc.alteration, mode)
          tonicized_keys.insert(0, tonicized_key)
          current_key = tonicized_key
     degree = special.scale_degree
     degree_alteration = special.scale_degree_alteration
     special.root = current_key.scale_degree(common.roman_to_int[degree], degree_alteration)
     harmalysis.chord = special
     return harmalysis

@v_args(inline=True)
class RomanParser(Transformer):
     ##################
     ## Parsing the key
     ##################
     # Key scales
     major_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'major')
     major_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'major')
     default_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'default_minor')
     default_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'default_minor')
     natural_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'natural_minor')
     natural_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'natural_minor')
     harmonic_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'harmonic_minor')
     harmonic_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'harmonic_minor')
     melodic_minor_key = lambda self, letter: harmalysis_classes.Key(letter, None, 'ascending_melodic_minor')
     melodic_minor_key_with_alteration = lambda self, letter, alteration: harmalysis_classes.Key(letter, alteration, 'ascending_melodic_minor')
     # Key types
     key_as_reference = lambda self, _: 'reference'
     key_as_established = lambda self, _: 'established'
     # Key
     key = lambda self, key_definition, key_function: (key_definition, key_function)
     ##########################
     ## Parsing a tertian chord
     ##########################
     # Triad
     major_triad = lambda self, scale_degree: ('major_triad', str(scale_degree), None)
     major_triad_with_alteration = lambda self, alteration, scale_degree: ('major_triad', str(scale_degree), str(alteration))
     minor_triad = lambda self, scale_degree: ('minor_triad', str(scale_degree), None)
     minor_triad_with_alteration = lambda self, alteration, scale_degree: ('minor_triad', str(scale_degree), str(alteration))
     augmented_triad = lambda self, scale_degree, _: ('augmented_triad', str(scale_degree), None)
     augmented_triad_with_alteration = lambda self, alteration, scale_degree, _: ('augmented_triad', str(scale_degree), str(alteration))
     diminished_triad = lambda self, scale_degree, _: ('diminished_triad', str(scale_degree), None)
     diminished_triad_with_alteration = lambda self, alteration, scale_degree, _: ('diminished_triad', str(scale_degree), str(alteration))
     # Inversions by number
     triad_inversion_by_number = int
     seventhchord_inversion_by_number = int
     # Inversions by letter
     inversion_by_letter = str
     # Added intervals
     added_seventh_diatonic = int
     added_seventh_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_ninth_diatonic = int
     added_ninth_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_eleventh_diatonic = int
     added_eleventh_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     added_thirteenth_diatonic = int
     added_thirteenth_with_quality = lambda self, quality, interval: interval.IntervalSpelling(str(quality), int(interval))
     # Missing intervals
     missing_intervals_triad = list
     missing_intervals_seventhchord = list
     missing_intervals_ninthchord = list
     missing_intervals_eleventhchord = list
     missing_intervals_thirteenthchord = list
     # Tertian
     tertian_triad = lambda self, triad, missing_intervals: _tertian_chord(triad, missing_intervals)
     tertian_triad_with_inversion_by_number = lambda self, triad, inversion_by_number, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_number=inversion_by_number)
     tertian_seventh_with_inversion_by_number = lambda self, triad, inversion_by_number, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_number=inversion_by_number, added_interval=7)
     tertian_triad_with_inversion_by_letter = lambda self, triad, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter)
     tertian_seventh = lambda self, triad, added_seventh, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_seventh)
     tertian_seventh_with_inversion_by_letter = lambda self, triad, added_seventh, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_seventh)
     tertian_ninth = lambda self, triad, added_ninth, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_ninth)
     tertian_ninth_with_inversion_by_letter = lambda self, triad, added_ninth, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_ninth)
     tertian_eleventh = lambda self, triad, added_eleventh, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_eleventh)
     tertian_eleventh_with_inversion_by_letter = lambda self, triad, added_eleventh, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_eleventh)
     tertian_thirteenth = lambda self, triad, added_thirteenth, missing_intervals: _tertian_chord(triad, missing_intervals, added_interval=added_thirteenth)
     tertian_thirteenth_with_inversion_by_letter = lambda self, triad, added_thirteenth, inversion_by_letter, missing_intervals: _tertian_chord(triad, missing_intervals, inversion_by_letter=inversion_by_letter, added_interval=added_thirteenth)
     ##########################
     ## Parsing a special chord
     ##########################
     # Augmented_sixths
     special_chord_name = str
     special_german = lambda self, name: _special_chord(name)
     special_german_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_german_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     special_italian = lambda self, name: _special_chord(name)
     special_italian_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_italian_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     special_french = lambda self, name: _special_chord(name)
     special_french_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_french_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     # Neapolitan
     special_neapolitan = lambda self, name: _special_chord(name)
     special_neapolitan_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_neapolitan_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     # Tristan
     special_tristan = lambda self, name: _special_chord(name)
     # Half diminished seventh
     special_halfdiminished = lambda self, name: _special_chord(name)
     special_halfdiminished_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_halfdiminished_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     # Cadential six-four
     special_cadential = lambda self, name: _special_chord(name)
     # Common-tone diminished
     special_commontone = lambda self, name: _special_chord(name)
     special_commontone_with_inversion_by_letter = lambda self, name, inversion: _special_chord(name, inversion_by_letter=inversion)
     special_commontone_with_inversion_by_number = lambda self, name, inversion: _special_chord(name, inversion_by_number=inversion)
     ########################
     ## Parsing tonicizations
     ########################
     by_scale_degree_major = lambda self, degree: (None, degree.lower(), "major")
     by_scale_degree_minor = lambda self, degree: (None, degree, "default_minor")
     by_scale_degree_neapolitan = lambda self, degree: ('b', "ii", "major")
     tonicization = lambda self, *args: list(args)
     #############################
     ## Parsing a harmalysis entry
     #############################
     # Tertian chords
     harmalysis_tertian = lambda self, tertian: _harmalysis_tertian(tertian)
     harmalysis_tertian_with_key = lambda self, key, tertian: _harmalysis_tertian(tertian, key_function=key)
     harmalysis_tertian_with_tonicization = lambda self, tertian, tonicizations: _harmalysis_tertian(tertian, tonicizations=tonicizations)
     harmalysis_tertian_with_key_and_tonicization = lambda self, key, tertian, tonicizations: _harmalysis_tertian(tertian, key_function=key, tonicizations=tonicizations)
     # Special chords
     harmalysis_special = lambda self, special: _harmalysis_special(special)
     harmalysis_special_with_key = lambda self, key, special: _harmalysis_special(special, key_function=key)
     harmalysis_special_with_tonicization = lambda self, special, tonicizations: _harmalysis_special(special, tonicizations=tonicizations)
     harmalysis_special_with_key_and_tonicization = lambda self, key, special, tonicizations: _harmalysis_special(special, key_function=key, tonicizations=tonicizations)


grammarfile = 'harmalysis_roman.lark'
parser = Lark(open(grammarfile).read())
pngs_folder = 'ast_pngs/'

def create_filename(query):
     f = query.replace(":", "_colon_")
     f = f.replace("=", "_equal_")
     f = f.replace(">", "_gt_")
     f = f.replace("/", "_slash_")
     f = f.replace("|", "_pipe_")
     f = f.replace("?", "_questionmark_")
     f = f.replace("#", "_sharp_")
     f = f.replace("+", "_plus_")
     f = f.replace("(", "_parenthesisl_")
     f = f.replace(")", "_parenthesisr_")
     f = f.replace("[", "_bracketl_")
     f = f.replace("]", "_bracketr_")
     return pngs_folder + f + ".png"

def parse(query, full_tree=False, create_png=True):
     ast = parser.parse(query)
     if create_png:
          filename = create_filename(query)
          tree.pydot__tree_to_png(ast, filename)
     if full_tree:
          return ast
     return RomanParser().transform(ast)

if __name__ == '__main__':
     ast = parse(sys.argv[1], full_tree=True)
     print(RomanParser().transform(ast))
     tree.pydot__tree_to_png(ast, 'ast_pngs/harmalysis_roman.png')