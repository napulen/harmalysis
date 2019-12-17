# harmparser
A parser based on regular expressions for the **harm syntax http://www.humdrum.org/rep/harm/


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
- Self-contained
  - Any given label should be self-contained. There is no necessity for context. The only exception to this is the local key, which, for commodity, can be provided once and omitted in future labels. In any case, this is not compulsory and local keys can be provided at every label for maximum clarity.
  - When no local key is provided at the first label, C Major is assumed.
- Immediately available for annotation within music notation editors
  - As a plain-text system, the syntax can be annotated as a lyric in music notation software without any additional software 

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

