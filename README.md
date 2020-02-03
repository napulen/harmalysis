# Notating roman numeral analysis

## A quick reference
```python
# Using the default key (C Major)
I           # C Major triad
IV          # F Major triad
V7          # G Dominant seventh chord

# Using a reference key
a:i         # A Minor triad
a:viio7     # G# Fully-diminished seventh chord
a:VI        # F Major triad

# Establishing a new key
I           # C Major triad
iii         # E Minor triad
V7/V        # D Dominant seventh chord
G=>:I       # G Major triad
IV          # C Major triad
ii7         # A Minor seventh chord
V           # D Major triad

# Use of special chords and inversions
f=>:i       # F Minor triad
viio7/ii    # F# Fully-diminished seventh chord
iio         # G Diminished triad
V43/V       # G Dominant seventh chord, second inversion
V6          # C Major triad, first inversion
V7          # C Dominant seventh chord
i           # F Minor triad
V6/N        # Db Major triad, first inversion (Dominant of the Neapolitan)
N           # Gb Major triad (Neapolitan of F Minor, root position)
i           # F Minor triad
```

## Guideline

A notation for roman numerals could be divided in three types of chords
- Tertian chords (e.g., `I`, `ii`, `V7`, etc.)
- Special chords (e.g., `Neapolitan`, `German augmented sixth`, etc.)
- Descriptive chords (e.g., `CM3D5`)

Let's start with Tertian chords.

## Tertian chords

The syntax of a tertian chord is based mainly on the definition of a **key**, **scale degree**, **added intervals**, and an **inversion**.

Other features like **missing intervals**, **tonicizations**, **modulations**, and **alternative notations** also exist and will be covered later.

### Key
Keys in the notation are divided in three categories, depending on their function:
- Reference key: A key given by the user as the reference key for a particular annotation.

Example:
```
F:I
```
A first degree major triad, `I`, in the context of `F Major`.

- Established key: Similar to a reference key, except that a established key becomes the new default key when no key is specified (default mechanism for annotating modulations).

Example:
```
F=>:I
IV
```

A first degree major triad, `I`, in the context of `F Major`. The second annotation corresponds to a `IV` degree in `F Major`, namely, `Bb Major`.

- Applied key: The applied key is the key from which the roman numeral is interpreted

Example:
```python
C=>:V/V     # G Major is the applied key, 
            # roman numeral is V of G Major (D Major triad)

V/V/V       # D Major is the applied key, 
            # roman numeral is V of D Major (A Major triad)
```

### Scale degrees (or roman numerals)
- Scale degrees consist of the symbols `I-VII` and `i-vii`
- The notation for roman numerals is **case sensitive**
- The reason why it is case sensitive is because roman numerals provide two assets of information
  - The **root** of the chord with respect to a key, given by the roman numeral itself, and,
  - The quality of the third accompanying that root, given by the **case** of the roman numeral

For example:

`I` - The root is the first degree of the establshed key, and it is accompanied by a major third

`i` - The root is the first degree of the establshed key, and it is accompanied by a minor third

It might seem weird to denote the root of the chord and (only) its third with the scale degree.

What about the fifth of the triad?

## Behavior of the fifth

By default, the fifth of the chord is a **perfect fifth**, therefore, in major and minor triads, it is not necessary to add any additional symbol to denote the triad other than:
- The scale degree
- The case of the scale degree

