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
import harmalysis.common as common
from harmalysis.classes.interval import IntervalSpelling
from harmalysis.classes.chord import DescriptiveChord, InvertibleChord, TertianChord, AugmentedSixthChord, NeapolitanChord, HalfDiminishedChord, CadentialSixFourChord, CommonToneDiminishedChord
from harmalysis.classes.harmalysis import Harmalysis
from harmalysis.classes.key import Key
from harmalysis.classes.pitch_class import PitchClassSpelling
import pathlib
import sys
import os


def _tertian_chord(triad, missing_intervals, inversion_by_number=None, inversion_by_letter=None, added_interval=None):
    tertian = TertianChord()
    triad_quality, scale_degree, alteration = triad
    tertian.set_scale_degree(scale_degree, alteration)
    tertian.set_triad_quality(triad_quality)
    # Handling inversions
    if inversion_by_number:
        tertian.set_inversion_by_number(inversion_by_number)
    elif inversion_by_letter:
        tertian.set_inversion_by_letter(inversion_by_letter)
    # Handling added intervals
    diatonic_intervals = []
    if added_interval:
        if isinstance(added_interval, IntervalSpelling):
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
        special = AugmentedSixthChord('german')
    elif name == 'Fr':
        special = AugmentedSixthChord('french')
    elif name == 'It' or name == "Lt":
        special = AugmentedSixthChord('italian')
    elif name == "N":
        special = NeapolitanChord()
    elif name == "Cad" or name == "Cad64":
        special = CadentialSixFourChord()
    elif name == "CTo" or name == "CTo7":
        special = CommonToneDiminishedChord()
    elif name == "vii0":
        special = HalfDiminishedChord()
    # TODO: Tristan chord
    # Handling inversions
    if inversion_by_number:
        special.set_inversion_by_number(inversion_by_number)
    elif inversion_by_letter:
        special.set_inversion_by_letter(inversion_by_letter)
    return special


def _descriptive_letter(pitch_class, intervals):
    descriptive_chord = DescriptiveChord()
    descriptive_chord.root = pitch_class
    for quality, step in zip(intervals[::2], intervals[1::2]):
        descriptive_chord.add_interval(IntervalSpelling(str(quality), int(step)))
    return descriptive_chord


def _descriptive_degree(scale_degree, intervals):
    descriptive_chord = DescriptiveChord()
    alteration, degree = scale_degree
    descriptive_chord.set_scale_degree(degree, alteration)
    for quality, step in zip(intervals[::2], intervals[1::2]):
        descriptive_chord.add_interval(IntervalSpelling(str(quality), int(step)))
    return descriptive_chord


def _harmalysis_tertian(tertian, key_function=None, tonicizations=[]):
    harmalysis = Harmalysis()
    if key_function:
        main_key, function = key_function
        if function == 'reference':
            harmalysis.reference_key = main_key
        elif function == 'established':
            Harmalysis.established_key = main_key
    else:
        main_key = Harmalysis.established_key
    tonicized_keys = []
    if tonicizations:
        secondary_key = main_key
        for tonicization in reversed(tonicizations):
            alteration, degree, mode = tonicization
            tonicized_pc = secondary_key.scale_degree(degree, alteration)
            tonicized_key = Key(tonicized_pc.note_letter, tonicized_pc.alteration, mode)
            tonicized_keys.insert(0, tonicized_key)
            secondary_key = tonicized_key
        harmalysis.secondary_key = secondary_key
    harmalysis.tonicized_keys = tonicized_keys
    harmalysis.main_key = main_key
    tertian_chord, diatonic_intervals = tertian
    degree = tertian_chord.scale_degree
    degree_alteration = tertian_chord.scale_degree_alteration
    root_diatonic_step = common.roman_to_int[degree]
    if harmalysis.secondary_key:
        tertian_chord.root = harmalysis.secondary_key.scale_degree(degree, degree_alteration)
        for diatonic in diatonic_intervals:
            interval = harmalysis.secondary_key.mode.step_to_interval_spelling(diatonic, mode=root_diatonic_step)
            tertian_chord.add_interval(interval)
    else:
        tertian_chord.root = harmalysis.main_key.scale_degree(degree, degree_alteration)
        for diatonic in diatonic_intervals:
            interval = harmalysis.main_key.mode.step_to_interval_spelling(diatonic, mode=root_diatonic_step)
            tertian_chord.add_interval(interval)
    harmalysis.chord = tertian_chord
    return harmalysis


def _harmalysis_special(special, key_function=None, tonicizations=[]):
    harmalysis = Harmalysis()
    if key_function:
        main_key, function = key_function
        if function == 'reference':
            harmalysis.reference_key = main_key
        elif function == 'established':
            Harmalysis.established_key = main_key
    else:
        main_key = Harmalysis.established_key
    tonicized_keys = []
    if tonicizations:
        secondary_key = main_key
        for tonicization in reversed(tonicizations):
            alteration, degree, mode = tonicization
            tonicized_pc = secondary_key.scale_degree(degree, alteration)
            tonicized_key = Key(tonicized_pc.note_letter, tonicized_pc.alteration, mode)
            tonicized_keys.insert(0, tonicized_key)
            secondary_key = tonicized_key
        harmalysis.secondary_key = secondary_key
    harmalysis.tonicized_keys = tonicized_keys
    harmalysis.main_key = main_key
    degree = special.scale_degree
    degree_alteration = special.scale_degree_alteration
    if harmalysis.secondary_key:
        if type(special) == CadentialSixFourChord:
            if harmalysis.secondary_key.scale == 'major':
                special.set_as_major()
            else:
                special.set_as_minor()
            degree = special.scale_degree
        special.root = harmalysis.secondary_key.scale_degree(degree, degree_alteration)

    else:
        if type(special) == CadentialSixFourChord:
            if harmalysis.main_key.scale == 'major':
                special.set_as_major()
            else:
                special.set_as_minor()
            degree = special.scale_degree
        special.root = harmalysis.main_key.scale_degree(degree, degree_alteration)

    harmalysis.chord = special
    return harmalysis


def _harmalysis_descriptive_letter(descriptive):
    harmalysis = Harmalysis()
    harmalysis.chord = descriptive
    return harmalysis


def _harmalysis_descriptive_degree(descriptive, key_function=None):
    harmalysis = Harmalysis()
    if key_function:
        main_key, function = key_function
        if function == 'reference':
            harmalysis.reference_key = main_key
        elif function == 'established':
            Harmalysis.established_key = main_key
    else:
        main_key = Harmalysis.established_key
    harmalysis.main_key = main_key
    degree = descriptive.scale_degree
    alteration = descriptive.scale_degree_alteration
    descriptive.root = main_key.scale_degree(degree, alteration)
    harmalysis.chord = descriptive
    return harmalysis


@v_args(inline=True)
class RomanParser(Transformer):
    ##################
    ## Parsing the key
    ##################
    # Key scales
    major_key = lambda self, letter: Key(letter, None, 'major')
    major_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'major')
    default_minor_key = lambda self, letter: Key(letter, None, 'minor')
    default_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'minor')
    natural_minor_key = lambda self, letter: Key(letter, None, 'natural_minor')
    natural_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'natural_minor')
    harmonic_minor_key = lambda self, letter: Key(letter, None, 'harmonic_minor')
    harmonic_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'harmonic_minor')
    melodic_minor_key = lambda self, letter: Key(letter, None, 'ascending_melodic_minor')
    melodic_minor_key_with_alteration = lambda self, letter, alteration: Key(letter, alteration, 'ascending_melodic_minor')
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
    added_seventh_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
    added_ninth_diatonic = int
    added_ninth_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
    added_eleventh_diatonic = int
    added_eleventh_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
    added_thirteenth_diatonic = int
    added_thirteenth_with_quality = lambda self, quality, interval: IntervalSpelling(str(quality), int(interval))
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
    #############################
    ## Parsing descriptive chords
    #############################
    pitch_class = lambda self, letter: PitchClassSpelling(letter)
    pitch_class_with_alteration = lambda self, letter, alteration: PitchClassSpelling(letter, alteration)
    descriptive_intervals = lambda self, *args: list(args)
    scale_degree = lambda self, degree: (None, degree.lower())
    scale_degree_with_alteration = lambda self, alteration, degree: (alteration, degree.lower())
    descriptive_chord_by_letter = lambda self, pitch_class, intervals: _descriptive_letter(pitch_class, intervals)
    descriptive_chord_by_degree = lambda self, scale_degree, intervals: _descriptive_degree(scale_degree, intervals)
    ########################
    ## Parsing tonicizations
    ########################
    by_scale_degree_major = lambda self, degree: (None, str(degree).lower(), "major")
    by_scale_degree_major_with_alteration = lambda self, alteration, degree: (str(alteration), str(degree), "major")
    by_scale_degree_minor = lambda self, degree: (None, str(degree), "minor")
    by_scale_degree_minor_with_alteration = lambda self, alteration, degree: (str(alteration), str(degree), "minor")
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
    # Descriptive chords
    harmalysis_descriptive_by_letter = lambda self, descriptive: _harmalysis_descriptive_letter(descriptive)
    harmalysis_descriptive_by_degree = lambda self, descriptive: _harmalysis_descriptive_degree(descriptive)
    harmalysis_descriptive_by_degree_with_key = lambda self, key_function, descriptive: _harmalysis_descriptive_degree(descriptive)

current_dir = pathlib.Path(__file__).parent.absolute()
grammarfile = os.path.join(str(current_dir), 'roman.lark')
parser = Lark(open(grammarfile).read())
pngs_folder = os.path.join(str(current_dir), 'ast_pngs/')

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

def parse(query, full_tree=False, create_png=False):
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