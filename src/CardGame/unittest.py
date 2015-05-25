"""
Created on 17 May 2015

@author: andy
"""

import unittest
import CardGame


class TestCard(unittest.TestCase):
    """ Test the card class."""

    def test_init_valid(self):
        valid_values = ((1, 1), (2, 4), (3, 11), (4, 13))
        for suit, rank in valid_values:
            card1 = CardGame.Card(suit, rank)
            self.assertEqual(card1.suit, suit)
            self.assertEqual(card1.rank, rank)

    def test_init_invalid(self):
        invalid_values = ((0, 0), (7, 1), (3, 15))
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


class TestPile(unittest.TestCase):

    def test_empty_pile(self):
        pile_name = "Test pile"
        pile = CardGame.Pile(pile_name)
        self.assertEqual(pile.name, pile_name)
        self.assertTrue(pile.is_empty())
        self.assertEqual(pile.count(), 0)

    def test_one_card(self):
        pile_name = "Test pile"
        pile = CardGame.Pile(pile_name)
        # Add one card
        pile.add(CardGame.Card(1, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 1)
        # Take one card
        card1 = pile.take()
        self.assertTrue(pile.is_empty())
        self.assertEqual(pile.count(), 0)
        self.assertEqual(card1.suit, 1)
        self.assertEqual(card1.rank, 9)
        #  Push one card
        pile.push(CardGame.Card(2, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 1)
        # Pop one card
        card1 = pile.pop()
        self.assertTrue(pile.is_empty())
        self.assertEqual(pile.count(), 0)
        self.assertEqual(card1.suit, 2)
        self.assertEqual(card1.rank, 9)

    def test_many_cards(self):
        pile_name = "Test pile"
        pile = CardGame.Pile(pile_name)
        # Add one card
        pile.add(CardGame.Card(1, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 1)
        # Add one card.
        pile.add(CardGame.Card(2, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 2)
        # Add one card.
        pile.add(CardGame.Card(3, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 3)
        # Add one card.
        pile.add(CardGame.Card(4, 9))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 4)
        # Delete one card from the middle of the pile.
        self.assertTrue(pile.remove(CardGame.Card(3, 9)))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 3)
        # Try to delete one card not in the pile.
        self.assertFalse(pile.remove(CardGame.Card(3, 10)))
        self.assertFalse(pile.is_empty())
        self.assertEqual(pile.count(), 3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
