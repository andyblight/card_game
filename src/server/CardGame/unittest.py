"""
Created on 17 May 2015

@author: andy
"""
# pylint: disable=too-many-public-methods

import unittest
import sys
import CardGame


class TestCard(unittest.TestCase):
    """ Test the card class."""

    def test_init_valid(self):
        """ ."""
        valid_values = ((1, 1), (2, 4), (3, 11), (4, 13), (5, 14))
        for suit, rank in valid_values:
            card1 = CardGame.Card(suit, rank)
            self.assertEqual(card1.suit, suit)
            self.assertEqual(card1.rank, rank)

    def test_init_invalid(self):
        """ ."""
        invalid_values = ((0, 0), (7, 1), (3, 15))
        for suit, rank in invalid_values:
            dummy = self.assertRaises(ValueError, CardGame.Card, suit, rank)

    def test_str(self):
        """ ."""
        valid_values = ((CardGame.Suit.Hearts,   CardGame.Rank.Ace,
                         "Hearts", "Ace"),
                        (CardGame.Suit.Diamonds, CardGame.Rank.Four,
                         "Diamonds", "Four"),
                        (CardGame.Suit.Clubs, CardGame.Rank.Ten,
                         "Clubs", "Ten"),
                        (CardGame.Suit.Clubs, CardGame.Rank.Jack,
                         "Clubs", "Jack"),
                        (CardGame.Suit.Spades, CardGame.Rank.Queen,
                         "Spades", "Queen"),
                        (CardGame.Suit.Spades, CardGame.Rank.King,
                         "Spades", "King"),
                        (CardGame.Suit.Red, CardGame.Rank.Joker,
                         "Red", "Joker"),
                        (CardGame.Suit.Black, CardGame.Rank.Joker,
                         "Black", "Joker"))
        for suit, rank, suit_name, rank_name in valid_values:
            card_str = rank_name + " " + suit_name
            card = CardGame.Card(suit, rank)
            self.assertEqual(card_str, card.__str__())


class TestPile(unittest.TestCase):
    """."""

    def test_empty_pile(self):
        """ ."""
        pile_name = "Test pile"
        pile = CardGame.Pile(pile_name)
        self.assertEqual(pile.name, pile_name)
        self.assertTrue(pile.is_empty())
        self.assertEqual(pile.count(), 0)

    def test_one_card(self):
        """ ."""
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
        """ ."""
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


class TestPlayers(unittest.TestCase):
    """."""

    def test_rounds(self):
        """."""
        players = CardGame.Players
        player = CardGame.Player("Andy")
        player.is_dealer = True
        players.append(player)
        player = CardGame.Player("Brian")
        players.append(player)
        player = CardGame.Player("Colin")
        players.append(player)
        player = CardGame.Player("David")
        players.append(player)
        # Iterate over players one shot, clockwise
        expected_player_list = (1, 2, 3, 0)
        player_list = list()
        starting_player_num = players.get_player_num_left_of_dealer()
        player_num = players.start_round(starting_player_num, False)
        while player_num is not -1:
            player_list.append(player_num)
            player_num = players.get_next_player_num_for_round()
        self.assertEqual(player_list, expected_player_list)

if __name__ == "__main__":
    sys.argv = ['', 'Test.testName']
    unittest.main()
