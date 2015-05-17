"""
Created on 17 May 2015

@author: andy
"""

import unittest
import CardGame


class TestCard(unittest.TestCase):

    def test_init_valid(self):
        valid_values = ((1, 1), (2, 4), (3, 11), (4, 13))
        for suit, rank in valid_values:
            card1 = CardGame.Card(suit, rank)
            self.assertEqual(card1.suit, suit)
            self.assertEqual(card1.rank, rank)

    def test_init_invalid(self):
        invalid_values = ((0, 0), (5, 1), (3, 14), (6, 20))
        for suit, rank in invalid_values:
            dummy = self.assertRaises(ValueError, CardGame.Card, suit, rank)

    def test_str(self):
        valid_values = ((1, 1, "Hearts", "Ace"),
                        (2, 4, "Diamonds", "Four"),
                        (3, 10, "Clubs", "Ten"),
                        (3, 11, "Clubs", "Jack"),
                        (4, 12, "Spades", "Queen"),
                        (4, 13, "Spades", "King"))
        for suit, rank, suit_name, rank_name in valid_values:
            suit_split = suit_name.partition(".")
            rank_spilt = rank_name.partition(".")
            card_string = rank_spilt[2] + " of " + suit_split[2]
            card1 = CardGame.Card(suit, rank)
            self.assertEqual(card_string, card1.__str__())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
