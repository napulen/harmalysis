# Harmalysis
## A language for encoding roman numeral analysis

# Quick start

The easiest way to test the language is to download the pip package

```
pip install harmalysis
```

and try the harmalysis interpreter

```
python -m harmalysis
```

Try some entries in the interpreter. Here is a quick reference of possible annotations.


## Quick reference
```python
# Using the default key (C Major)
I           # C Major triad
IV          # F Major triad
V7          # G Dominant seventh chord
```

```python
# Using a reference key
a:i         # A Minor triad
a:viio7     # G# Fully-diminished seventh chord
a:VI        # F Major triad
```

```python
# Establishing a new key
I           # C Major triad
iii         # E Minor triad
V7/V        # D Dominant seventh chord
G=>:I       # G Major triad
IV          # C Major triad
ii7         # A Minor seventh chord
V           # D Major triad
```

```python
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

# Guideline

The chord annotations in harmalysis can be divided in three types of chords:

- Tertian chords (e.g., `I`, `ii`, `V7`, etc.)
- Special chords (e.g., `Neapolitan`, `German augmented sixth`, etc.)
- Descriptive chords (e.g., `CM3D5`)

## Tertian chords

The syntax of a tertian chord is based mainly on the definition of a **key**, **scale degree**, **added intervals**, and an **inversion**.

Other features like **missing intervals** and **alternative notations** are also available.

### Key
Keys in the notation are divided in three categories, depending on their function:
- Reference key: A key given by the user as the reference key for a particular annotation.

Example:
```
F:I
```
A first degree major triad, `I`, in the context of `F Major`.

- Established key: Similar to a reference key, except that a established key becomes the new default key when no key is specified.

This is the suggested notation for establishing a key at the beginning of the piece, or after a modulation.

Example:
```
F=>:I
IV # <-- The IV degree of F major (Bb major triad)
```

The first annotation corresponds to a first degree major triad, `I`, in the context of `F Major`. 

The second annotation corresponds to a `IV` degree in `F Major`, namely, `Bb Major`.

- Tonicized key: The tonicized key is the key from which the roman numeral is interpreted

Example:
```python
C=>:V/V     # G Major is the tonicized key, 
            # roman numeral is V of G Major (D Major triad)

V/V/V       # D Major is the tonicized key, 
            # roman numeral is V of D Major (A Major triad)
```

In the case of multiple *levels* of tonicization (e.g., the `V/V/V` annotation), the sequence of tonicized keys are resolved recursively from right to left until a resulting key is found. This key will be the tonicized key. 

> Nevertheless, `harmalysis` keeps track of all the intermediate tonicizations and they can be retrieved from the returned object.


### Scale degrees (or roman numerals)
- Scale degrees consist of the symbols `I-VII` and `i-vii`
- The notation for roman numerals is **case sensitive**
- They are case sensitive because they provide two assets of information
  - The **root** of the chord with respect to a key, given by the roman numeral itself, and,
  - The quality of the third accompanying that root, given by the **case** of the roman numeral

For example:

`I` - The root is the first degree of the establshed key, and it is accompanied by a major third

`i` - The root is the first degree of the establshed key, and it is accompanied by a minor third

It might seem weird to denote the root of the chord and (only) its third with the scale degree.

What about the fifth of the triad?

## Triads

By default, the fifth of the chord is a **perfect fifth**.

### Major and minor triads

 Therefore, major and minor triads can be described with only a case-sensitive scale degree (lower-case for minor, and upper-case for major triads))

 ```python
 I    # C major
 i    # c minor
 ```

 ### Augmented triads

 Augmented triads are denoted by the `+` symbol after the scale degree.

 ```python
 c:III+    # Eb augmented triad
 ```

 Augmented triads are only accepted when the scale degree is upper cased. That is, it implies a major triad. In this context, the `+` can be interpreted as an *augmented fifth* instead of a perfect fifth.

 ### Diminished triads

 Diminished triads are denoted by the `o` symbol after the scale degree.

 ```python
 c:viio    # B diminished triad
 ```

 Diminished triads are only accepted when the scale degree is lower cased. That is, it implies a minor triad. In this context, the `o` can be interpreted as a *diminished fifth* instead of a perfect fifth.
