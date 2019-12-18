# harmalysis
A grammar (and language) for harmonic analysis and roman numerals. Based on and extending the [**harm](http://www.humdrum.org/rep/harm/) syntax

# An improved syntax for encoding Roman Numerals

## Philosophy of the syntax
- Compact
- Resembling music theory analyses
- Systematic over music-theoretically complete
  - The vocabulary of chords is limited
  - Unlike `**harm`, you cannot encode something like this: `A4m7m10`
  - This is inconvenient for some people, but it has its benefits: Every RNA entry can be resolved to a chord label
  - Reduces the vocabulary of chords, something desirable for machine learning algorithms
  - (Forces the user to spend more time analyzing the fragment, determining non-chord tones, and other dimensions of the harmonic context, rather than spelling out lots of added intervals in a given entry)
- Agnostic to the music encoding format
  - Encoded as plain-text in a dedicated field (e.g. `<harmony>`) or simply as a lyric
  - The syntax can be used in any encoding format that allows to align text with a musical event (e.g., MusicXML, Humdrum, MEI, MIDI)
- Stand-alone
  - Any given label should be self-explanatory. There is no necessity for context. The only exception to this is the local key, which, for commodity, can be provided once and omitted in future labels. In any case, this is not compulsory and local keys can be provided at every label for maximum clarity.
  - When no local key is provided at the first label, C Major is assumed.
- Immediately available for annotation within music notation editors
  - As a plain-text system, the syntax can be annotated as a lyric in music notation software without any additional software
- Derivate the machine-readable from the human-readable and not the other way around

# Breaking down the encoding of Roman Numeral Analysis
- A label like `I` or `i`, implicitly gives us the following information:
  - We talk about a triad
  - A triad with the root of the chord as a diatonic degree in the local key
  - Whether the third of the triad is a `major` third (upper case degree) or a `minor` third (lower case degree)
  - Assumes a `perfect 5th`
- What the label `I` or `i`, does not tell us:
  - The **quality** of the triad
  - We don't know whether it is a `major`, `minor`, `augmented` or `diminished` triad. We need the operators following the degree `o` and `+` to know whether we talk about a diminished or augmented triad
  - The diatonic triad that emerges from that given scale degree
    - Examples of this include `III` and `vii` in the minor mode
    - In the diatonic construction of the triads based on these scale degrees, these should be `Augmented` and `Diminished` chords, respectively, however, when we refer to a diminished seventh degree we typically write it as `viio`, and a major third degree as `III`.

# Departures from `**harm` syntax
- The `++harm` is a superset of the `**harm` syntax
- In the `**harm` representation, the key context is provided through the regular mechanisms of the `**kern` representation
- In this syntax, the key context is provided within the label, enabling its use in other use cases, for example, where the change of key is not explicitly written in the score (music notation editors)
- The `**harm++` syntax *completes* the notation of the `**harm` syntax when this is not provided in the original syntax.
- The `augmented` type is only valid within major scale degrees (e.g., `i+` is an invalid label, but `I+` is valid)
- The `diminished` type is only valid within minor scale degrees (e.g., `Io` is an invalid label, whereas `io` is valid)
- Added intervals are provided for completeness with the `**harm` syntax, but they are discouraged (except for single added intervals, like 7th and 9ths)
- Adding an additional interval quality `x`, which means, missing interval
- In `**harm` and `**kern`, flats are encoded as `-`, in our syntax, `b` is also accepted as a flat symbol
- Allowing the encoding of half-diminished seventh chords with the shorthand `vii0`, which is used by MuseScore

# Kostka-Payne on Ninth, Evelenth, and Thirteenth chords

> Interesting as these chords may be, the triad and the seventh chord were really the standard fare of music in the ieghteenth and nineteenth centuries. True elevenths and thirteenths are rare before impressionism, which began in the late nineteenth century. Ninths occur throughout the tonal era, but the 9th of the chord often can be analyzed as a NCT and usually disappears before the chord resolves.



# About the notation of the language

## Accidentals

Sharps and flats are supported.

Sharps are encoded as `#`, flats can be encoded as `-` or `b`.

> Originally, the **harm syntax encodes flats as `-`, however, there is no particular reason for not using the `b` letter, which is more commonly used to denote a flat accidental. Therefore, the `harm++` syntax supports both forms

Double sharps are encoded as `##` or `x`, and double flats are encoded as either `--` (compatible with the `**harm` syntax) or `bb`.

## Note letters

The note letters (e.g., in the context of defining a key of *Eb minor*, `eb:`) are encoded as the letters `A`-`G` and `a`-`g`.

In certain contexts (e.g., defining a key), the syntax is case sensitive, lower-case letters denote minor keys and upper-case letters denote major keys.

## Scale degrees

In the grammar of the `harm++` language, scale degrees have been encoded as *terminal* symbols, which are parsed according to their conventional names:

```
TONIC_UPPERCASE : "I"
SUPERTONIC_UPPERCASE : "II"
MEDIANT_UPPERCASE : "III"
SUBDOMINANT_UPPERCASE : "IV"
DOMINANT_UPPERCASE : "V"
SUBDOMINANT_UPPERCASE : "VI"
SEVENTH_DEGREE_UPPERCASE : "VII"

TONIC_LOWERCASE : "i"
SUPERTONIC_LOWERCASE : "ii"
MEDIANT_LOWERCASE : "iii"
SUBDOMINANT_LOWERCASE : "iv"
DOMINANT_LOWERCASE : "v"
SUBDOMINANT_LOWERCASE : "vi"
SEVENTH_DEGREE_LOWERCASE : "vii"
```

Once again, in some contexts (e.g., tonicizations and triads) the syntax is case-sensitive, denoting major mode as upper-case roman numerals and minor mode as lower-case roman numerals.

> Note that the `SEVENTH_DEGREE` was not encoded as `LEADING_TONE`. This decision was made because of the dual role of the seventh degree as leading tone and subtonic (flattened seventh), which cannot be inferred from the grammar.

## Inversions

The language supports up to 11 possible inversions. This would imply that a chord with 12 different notes can be specified with its inversions using this language.

However, in most cases, harmonic analyses describe chords with either 3 or 4 notes, so the number of inversions is divided in three categories:

- Triad inversions: First and second inversions (e.g., 6 and 64), denoted with the letters `b` and `c`, respectively.
- Chord inversions: First, second, and third inversions (e.g., 65, 43, and 2), denoted with the letters `b`, `c`, and `d`, respectively.
- Extended-chord inversions: All letters in the range `b`-`l`

The special character `a` denotes a chord in root position, however, this is the default assumption by the syntax if no inversion is specified and can be safely omitted.

## Added intervals

The `**harm` syntax specifies that additional intervals can be added after the scale degree. This is also true for `harm++`, except for a few considerations:

- In a regular triadic-based chord, only one interval can be added
  - The supported intervals added on top of a triad are `7`, `9`, `11`, and `13`.
- The intervals can be preceded by their quality
```
MAJOR_INTERVAL : "M"
MINOR_INTERVAL : "m"
PERFECT_INTERVAL : "P"
AUGMENTED_INTERVAL : "A"
DIMINISHED_INTERVAL : "D"
DOUBLE_AUGMENTED_INTERVAL : "AA"
DOUBLE_DIMINISHED_INTERVAL : "DD"
```
- When no interval quality is specified (only the number), the interval is considered to be diatonic and it is based on the current key and scale degree.

## Missing intervals

The `harm++` language incorporates a new notation, missing intervals, which is not considered in the `**harm` syntax.

Missing intervals can be included in a roman numeral label by writing the corresponding number, preceded by the `x` symbol.

The only supported missing intervals are the `unison`, `third`, and `fifth`.

> By definition, the 7th is an added interval, therefore, it cannot be missing. If it is missing, then it should simply not be annotated

Missing intervals are only possible within triad-based chords, not special chords or descriptive chords.

> By definition, special chords are special instances of pitch-classes in a special context (e.g., cadential or german augmented sixth). If they are missing notes, then they do not fullfil the criteria to be annotated as such special chords.


## Special chords

The language supports a handful of *special chords*, which include these:

- Augmented sixth chords
  - German augmented sixth, `Ger` or `Gn`
  - Italian augmented sixth, `It`, or `Lt`
  - French augmented sixth, `Fr`

> In the `**harm` syntax, German augmented sixths are denoted as `Gn` and Italian augmented sixths as `Lt`. In `harm++`, the notations `Ger` and `It` have also been included, as they appear more often in music theory books.

- Neapolitan chord, `N`
- Tristan chord, `Tr`
- Half-diminished seventh, `vii0`
> The half-diminished seventh can be encoded as a triad-based chord as `viiom7`, however, the shorthand `vii0` is included given that it is the way that these chords are written in the MuseScore Campanella font
- Cadential six-four, `Cad` or `V64`
- Common-tone diminished seventh, `CTdim7`

The special chords have specific properties, for example, they support inversions according to the number of notes that they contain. For example, a german augmented sixth chord supports 3 inversions, whereas an italian augmented sixth only supports 2 inversions. A more extreme example of this is the cadential six-four chord, which does not support any inversion. If an inversion is specified for this chord, the language parser will throw an error.

> By definition, the cadential six-four has a form of I64. Whether it is the first degree in second inversion or the fifth degree with appoggiaturas is an open debate, however, it is agreed that the bass is always the fifth degree and therefore, there is no ambiguity of the bass as to require to specify an inversion. If the special chord is not to be used, this chord can also be encoded as `Ic` or `Vc`, but we recommend using the special chord notation.

## Descriptive chords

When a chord cannot be explained neither as a triad with an added interval (7th, 9th, 11th, or 13th) nor as a special chord, it can be described by its scale degree root and a series of added intervals. This notation has been implemented in order to support a similar mechanism in the `**harm` syntax.

Although the parser will attempt its best to explain a descriptive chord, their semantic interpretation is much less informative than a triad-based or special chord. Therefore, descriptive chords are discouraged and it is suggested to find a way to explain all the chords through the triad-based or special chords.

Special chords are prepended by the symbol `?` followed by a scale degree and a series of added intervals.

The supported intervals span from the unison to a fifteenth (two octaves above the bass), and 11 possible inversions.

The consistency of the inversions with the added intervals is not verified by the parser. For example, the chord `?IM3P5h` (Descriptive chord starting on the first degree, adding a major third, a perfect fifth, in seventh inversion) is a valid label. This is one of the reasons why we discourage their use.

