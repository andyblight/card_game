"""
Created on 17 May 2015

@author: andy
"""

from enum import IntEnum


class Suit(IntEnum):
    """ Suit of the Card. """
    Undefined = 0
    Hearts = 1
    Diamonds = 2
    Clubs = 3
    Spades = 4
    Red = 5
    Black = 6


class Rank(IntEnum):
    """ Ranks of the Card. """
    Undefined = 0
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Card:
    """ The Card class implements the basic methods for using a card. """

    def __init__(self, suit=Suit.Undefined, rank=Rank.Undefined):
        if ((1 <= suit <= 4) and (1 <= rank <= 13)):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = Suit.Undefined
            self.rank = Rank.Undefined
            raise ValueError("Parameter out of range")

    def __str__(self):
        suit_string = self.suit.__str__()
        rank_string = self.rank.__str__()
        suit_split = suit_string.partition(".")
        rank_spilt = rank_string.partition(".")
        return rank_spilt[2] + " of " + suit_split[2]
