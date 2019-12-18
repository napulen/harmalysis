from lark import Lark

grammar = '''

/////////////////////////////////
// Flats, sharps, and alterations
/////////////////////////////////
flat : "-" | "b"
double_flat : "--" | "bb"
sharp : "#"
double_sharp : "##" | "x"
alteration : flat
     | double_flat
     | sharp
     | double_sharp

///////////////////////////////////////////
// Lower-case, upper-case letters, and keys
///////////////////////////////////////////
lower_letter : "a" | "b" | "c" | "d" | "e" | "f" | "g"
upper_letter : "A" | "B" | "C" | "D" | "E" | "F" | "G"
letter : lower_letter | upper_letter
key: letter [alteration] ":"

////////////////
// Scale degrees
////////////////
upper_scale_degree : "I" | "II" | "III" | "IV" | "V" | "VI" | "VII"
lower_scale_degree : "i" | "ii" | "iii" | "iv" | "v" | "vi" | "vii"
scale_degree : upper_scale_degree | lower_scale_degree

/////////////
// Inversions
/////////////
no_inversion : "a"
first_inversion : "b"
second_inversion: "c"
third_inversion: "d"
fourth_inversion: "e"
fifth_inversion: "f"
sixth_inversion: "g"
seventh_inversion: "h"
eighth_inversion: "i"
ninth_inversion: "j"
tenth_inversion: "k"
eleventh_inversion: "l"

triad_inversion : no_inversion
                | first_inversion
                | second_inversion

chord_inversion : triad_inversion | third_inversion

extended_chord_inversion : chord_inversion
                         | fourth_inversion
                         | fifth_inversion
                         | sixth_inversion
                         | seventh_inversion
                         | eighth_inversion
                         | ninth_inversion
                         | tenth_inversion
                         | eleventh_inversion

//////////////////
// Added intervals
//////////////////
basic_added_intervals : "7" | "9" | "11" | "13"
all_valid_added_intervals : basic_added_intervals
               | "1"
               | "2"
               | "3"
               | "4"
               | "5"
               | "6"
               | "8"
               | "10"
               | "12"
               | "14"
               | "15"

major_interval : "M"
minor_interval : "m"
perfect_interval : "P"
augmented_interval : "A"
diminished_interval : "D"
double_augmented_interval : "AA"
double_diminished_interval : "DD"

interval_quality : major_interval
                 | minor_interval
                 | perfect_interval
                 | augmented_interval
                 | diminished_interval
                 | double_augmented_interval
                 | double_diminished_interval

basic_added_interval : [interval_quality] basic_added_intervals
any_added_interval : [interval_quality] all_valid_added_intervals

////////////////////
// Missing intervals
////////////////////
valid_missing_intervals : "1" | "3" | "5"
missing_interval_symbol : "x"
missing_interval : missing_interval_symbol valid_missing_intervals

////////////////////
// Triad alterations
////////////////////
diminished_triad_symbol : "o"
augmented_triad_symbol : "+"
major_triad : [alteration] upper_scale_degree
augmented_triad : major_triad augmented_triad_symbol
minor_triad : [alteration] lower_scale_degree
diminished_triad : minor_triad diminished_triad_symbol

/////////
// Triads
/////////
triad : major_triad
      | augmented_triad
      | minor_triad
      | diminished_triad

/////////////////////
// Triad-based chords
/////////////////////
triad_chord : triad missing_interval* [triad_inversion]
extended_triad_chord: triad basic_added_interval [chord_inversion]

/////////////////
// Special chords
/////////////////
german : "Ger" | "Gn"
italian : "Lt" | "It"
french : "Fr"
augmented_sixth : german [chord_inversion] | italian [triad_inversion] | french [chord_inversion]

neapolitan : "N"
tristan : "Tr"
half_diminished_seventh : "vii0"
cadential : "Cad" | "V64"
common_tone : "CTdim7" | "CTo7"

special_chord : augmented_sixth
              | neapolitan [triad_inversion]
              | tristan [chord_inversion]
              | half_diminished_seventh [chord_inversion]
              | cadential
              | common_tone [chord_inversion]


chord : triad_chord | extended_triad_chord | special_chord

'''

l = Lark(grammar, start='chord')