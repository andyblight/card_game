"""
Created on 17 May 2015

@author: andy
"""

import unittest
import CardGame


class TestCardClass(unittest.TestCase):

    # Tuple of suit, rank.
    valid_values = ((1, 1), (2, 4), (3, 11), (4, 13))
    invalid_values = ((0, 0), (5, 1), (3, 14), (6, 20))

    def test_init_valid(self):
        for suit, rank in self.valid_values:
            card1 = CardGame.Card(suit, rank)
            self.assertEqual(card1.rank, rank)
            self.assertEqual(card1.suit, suit)

    def test_init_invalid(self):
        for suit, rank in self.invalid_values:
            dummy = self.assertRaises(ValueError, CardGame.Card, suit, rank)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
