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
    Joker = 14


class Card:
    """ The Card class implements the basic methods for using a card. """

    def __init__(self, suit=Suit.Undefined, rank=Rank.Undefined):
        if (Suit.Undefined < suit <= Suit.Black) \
                and (Rank.Undefined <= rank <= Rank.Joker):
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
        card_str = rank_spilt[2] + " " + suit_split[2]
        # print("DBG Card " + card_str + ".")
        return card_str


class Pile:
    """The pile class holds number of cards in a stack."""

    def __init__(self, name=""):
        self.cards = []
        self.name = name

    def is_empty(self):
        """Returns True if empty."""
        return len(self.cards) == 0

    def count(self):
        """Returns the number of cards in the pile."""
        return len(self.cards)

    def add(self, card):
        """Add a card to the bottom of the pile."""
        self.cards.append(card)

    def take(self):
        """Remove a card from the bottom of the pile."""
        return self.cards.pop()

    def push(self, card):
        """Add a card to the top of the pile."""
        self.cards.insert(0, card)

    def pop(self):
        """Returns and removes the card from the top of the pile."""
        return self.cards.pop(0)

    def remove(self, card):
        """Removes a card from the pile with the same value as the given
        card."""
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False


class Hand(Pile):
    """class."""

    def __init__(self, name):
        Pile.__init__(self, name)

    def list(self):
        """Prints a list of all cards in a hand."""
        cards_str = self.name + " has "
        for i in range(len(self.cards)):
            cards_str = cards_str + self.cards[i].__str__() + ", "
        print(cards_str)


class Player():
    """ ."""

    def __init__(self, name):
        self.hand = Hand(name)

    def clear(self):
        self.hand.cards.clear()


class Deck(Pile):
    """class."""

    def __init__(self, name="Deck"):
        Pile.__init__(self, name)
        for suit in Suit:
            for rank in Rank:
                if (Suit.Hearts < suit < Suit.Red) \
                        and (Rank.Ace < rank < Rank.Joker):
                    self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffles the cards in the deck by swapping them."""
        import random
        num_cards = self.count()
        for dummy in range(1, 2):
            for i in range(num_cards):
                j = random.randrange(i, num_cards)
                self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def deal(self, players, num_cards=999):
        """Deals num_cards to each hand in hands."""
        for i in range(0, num_cards):
            for j in range(len(players)):
                # print("DEAL: card " + str(i) + ", player " + str(j))
                if self.is_empty():
                    break
                card = self.pop()
                hand = players[j].hand
                hand.add(card)


class CardGame():
    """Creates the deck and shuffles it."""

    def __init__(self):
        deck = Deck()
        deck.shuffle()
