import harmalysis
import itertools
import unittest

keys_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
keys_minor = [k.lower() for k in keys_major]
keys_major_minor = keys_major + keys_minor
alterations = ['#', '##', 'x', 'b', 'bb', '-', '--']
all_keys = ['{}{}'.format(k, a) for k, a in itertools.product(keys_major_minor, alterations)]


scale_degrees_major = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
scale_degrees_minor = [sd.lower() for sd in scale_degrees_major]
scale_degrees_diminished = ['{}o'.format(m) for m in scale_degrees_minor]
scale_degrees_augmented = ['{}+'.format(M) for M in scale_degrees_major]
all_triads = scale_degrees_major + scale_degrees_minor + scale_degrees_diminished + scale_degrees_augmented


triad_numeric_inversions = ['6', '64']
triad_inversions_by_letter = ['b', 'c']

tertian_added_intervals = ['7', '9', '11', '13']


class TestTertian(unittest.TestCase):
    def test_triad(self):
        sds = scale_degrees_major
        for sd in sds:
            with self.subTest(sd=sd):
                r = harmalysis.parse(sd)
                self.assertEqual(r.chord.scale_degree, sd)

    def test_triad_alteration(self):
        sds = list(itertools.product(alterations, scale_degrees_major))
        for alt, sd in sds:
            with self.subTest(sd=sd, alt=alt):
                r = harmalysis.parse(alt + sd)
                self.assertEqual(r.chord.scale_degree, sd)
                self.assertEqual(r.chord.scale_degree_alteration, alt)

    def test_all_major_keys(self):
        keys = list(itertools.product(keys_major, alterations + ['']))
        for key, alt in keys:
            with self.subTest(key=key, alt=alt):
                r = harmalysis.parse(key + alt + ':I')
                self.assertEqual(str(r.main_key.tonic), key + alt)

    def test_all_minor_keys(self):
        keys = list(itertools.product(keys_minor, alterations + ['']))
        for key, alt in keys:
            with self.subTest(key=key, alt=alt):
                r = harmalysis.parse(key + alt + ':i')
                self.assertEqual(str(r.main_key.tonic), key.upper() + alt)

    def test_diatonic_sevenths(self):
        queries = {
            'I7': 'CM3P5M7',
            'ii7': 'Dm3P5m7',
            'iii7': 'Em3P5m7',
            'IV7': 'FM3P5M7',
            'V7': 'GM3P5m7',
            'vi7': 'Am3P5m7',
            'viio7': 'Bm3D5m7'
        }
        for label, intervals in queries.items():
            with self.subTest(label=label, i=intervals):
                r = harmalysis.parse(label)
                self.assertEqual(str(r.chord), intervals)

    # TODO: test_diatonic_ninths
    # TODO: test_diatonic_elevenths
    # TODO: test_diatonic_thirteenths


if __name__ == '__main__':
    unittest.main()
