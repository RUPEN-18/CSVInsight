import io
import unittest
from csvinsight import profile

class ProfileTests(unittest.TestCase):
    def test_duplicates_and_missing(self):
        r = profile(io.StringIO('name,score\nA,10\nA,10\nB,\nC,20\n'))
        self.assertEqual(r['rows'], 4)
        self.assertEqual(r['duplicate_rows'], 1)
        self.assertEqual(r['column_profiles'][1]['missing'], 1)
        self.assertEqual(r['column_profiles'][1]['statistics']['median'], 10)
    def test_empty_columns(self):
        self.assertEqual(profile(io.StringIO('a,b\n'))['column_profiles'][0]['type'], 'empty')
    def test_bad_shape(self):
        with self.assertRaises(ValueError): profile(io.StringIO('a,b\n1\n'))
    def test_duplicate_header(self):
        with self.assertRaises(ValueError): profile(io.StringIO('a,a\n1,2\n'))
    def test_mixed_text(self):
        self.assertEqual(profile(io.StringIO('x\n1\nunknown\n'))['column_profiles'][0]['type'], 'text')
