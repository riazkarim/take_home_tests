from unittest import TestCase

from find_my_number import Keypad
from find_my_number import KeypadSequenceFinder

"""
Test classes for Keypad and KeypadSequenceFinder that test functionality given the sequence_length/max_vowels specified in the problem.
"""

class KeypadSequenceFinderTests(TestCase):
    def setUp(self):
        self.subject = KeypadSequenceFinder(keypad=Keypad(), sequence_length=10, max_vowels=2)

    def test_get_valid_next_moves(self):
        self.assertEqual(self.subject.get_valid_next_moves('A'), {'L', 'H'})
        self.assertEqual(self.subject.get_valid_next_moves('E'), {'N', 'H'})
        self.assertEqual(self.subject.get_valid_next_moves('C'), {'L', 'N', 'F', 'J'})
        self.assertEqual(self.subject.get_valid_next_moves('2'), {'G', 'I', 'K', 'O'})

    def test_get_sequence_count(self):
        self.assertEqual(self.subject.get_sequence_count('A',1, 1, ['A']), 30004)
        self.assertEqual(self.subject.get_sequence_count('B',1, 0, ['B']), 49154)
        self.assertEqual(self.subject.get_sequence_count('1', 1, 0, ['1']), 64287)

    def test_get_total_count(self):
        self.assertEqual(self.subject.get_total_count(), 1013398)

    def test_validate_sequence(self):
        self.assertEqual(self.subject.validate_sequence(['A', 'H', '3', 'J', 'C', 'F', 'M', 'D', 'O', '2']), True)
        self.assertEqual(self.subject.validate_sequence(['A', 'H', 'C', 'D', 'E', 'F', 'G', 'H', '1', '2']), False)


class KeypadTests(TestCase):
    def setUp(self):
        self.subject = Keypad()

    def test_get_key_position(self):
        self.assertEqual(self.subject.get_key_position('A'), (0, 0))
        self.assertEqual(self.subject.get_key_position('2'), (3, 2))
        self.assertRaises(ValueError, self.subject.get_key_position, 'U')

    def test_get_rows(self):
        self.assertEqual(self.subject.get_num_rows(), 4)

    def test_get_cols(self):
        self.assertEqual(self.subject.get_num_cols(3), 5)
        self.assertRaises(ValueError, self.subject.get_num_cols, 4)



