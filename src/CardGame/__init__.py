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

    def __str__(self):
        suit_string = IntEnum.__str__(self)
        suit_split = suit_string.partition(".")
        return suit_split[2]


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

    def __str__(self):
        rank_string = IntEnum.__str__(self)
        rank_split = rank_string.partition(".")
        return rank_split[2]


class Card:
    """ The Card class implements the basic methods for using a card. """

    def __init__(self, suit=Suit.Undefined, rank=Rank.Undefined):
        if (Suit.Undefined <= suit <= Suit.Black) \
                and (Rank.Undefined <= rank <= Rank.Joker):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = Suit.Undefined
            self.rank = Rank.Undefined
            raise ValueError("Parameter out of range")

    def __str__(self):
        card_str = str(self.rank) + " " + str(self.suit)
        # print("DBG Card " + card_str + ".")
        return card_str

    def value(self, trump_suit):  # pylint: disable=unused-argument
        """Returns the value of the card."""
        return int(self.rank)

    def is_black(self):
        """ Returns True is the suit is black."""
        return self.suit == Suit.Clubs or \
            self.suit == Suit.Spades or \
            self.suit == Suit.Black

    def is_red(self):
        """ Returns True is the suit is red."""
        return self.suit == Suit.Hearts or \
            self.suit == Suit.Diamonds or \
            self.suit == Suit.Red


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


class Hand(Pile):
    """class."""

    def __init__(self, name):
        Pile.__init__(self, name)

    def list(self):
        """Prints a list of all cards in a hand."""
        cards_str = self.name + " has "
        for i in range(len(self.cards)):
            cards_str = cards_str + str(self.cards[i]) + ", "
        print(cards_str)


class Player():
    """The player class has a one hand."""

    def __init__(self, name):
        self.hand = Hand(name)
        self.is_dealer = False

    def clear(self):
        """Clears the hand and dealer status of the player."""
        self.hand.cards.clear()
        self.is_dealer = False


class Players():
    """A list of player instances with the ability to add players and to
    iterate over the list of players in a circular fashion with a nominated
    player starting first."""

    def __init__(self):
        self.players = list()
        self.round_start_player = -1
        self.round_next_player = -1
        self.round_one_shot = True
        self.round_clockwise = True
        self.dealer_num = -1

    def __len__(self):
        return len(self.players)

    def append(self, player):
        """Appends the player."""
        self.players.append(player)

    def clear(self):
        """Clears the list of players."""
        self.players.clear()
        self.round_start_player = -1
        self.round_next_player = -1
        self.round_one_shot = True
        self.round_clockwise = True
        self.dealer_num = -1

    def reset(self):
        """Reset each player to the default state."""
        for player_num in range(len(self.players)):
            self.players[player_num].reset()

    def get_player(self, player_num):
        """Returns a copy of the player with player_num."""
        return self.players[player_num]

    def set_player(self, player_num, new_player):
        """Overwrites the player with player_num."""
        if 0 <= player_num <= len(self.players):
            self.players[player_num] = new_player
        else:
            raise IndexError

    def set_player_num_of_dealer(self, dealer_player_num):
        """Marks the given player as dealer."""
        for player_num in range(len(self.players)):
            if player_num == dealer_player_num:
                self.players[player_num].is_dealer = True
                self.dealer_num = player_num
            else:
                self.players[player_num].is_dealer = False

    def get_player_num_of_dealer(self):
        """Gets the number of the player marked as dealer."""
        return self.dealer_num

    def get_player_num_left_of_dealer(self):
        """Gets the number of the player to the left of the dealer."""
        player_num = self.dealer_num + 1
        player_num %= len(self.players)
        return player_num

    def get_player_num_right_of_dealer(self):
        """Gets the number of the player to the right of the dealer."""
        player_num = self.dealer_num - 1
        player_num %= len(self.players)
        return player_num

    def start_round(self, start_player_num, one_shot=True, clockwise=True):
        """Sets the starting player number and the type of round.
        Returns the value of start_player_num if in range, otherwise -1."""
        if 0 <= start_player_num <= len(self.players):
            self.round_start_player = start_player_num
            self.round_next_player = start_player_num
        else:
            self.round_start_player = -1
            self.round_next_player = -1
        self.round_one_shot = one_shot
        self.round_clockwise = clockwise
        # print("Start round: player", self.round_next_player,
        #      "one_shot", self.round_one_shot,
        #      "clockwise", self.round_clockwise)
        return self.round_next_player

    def get_next_player_num_for_round(self):
        """Gets the next player number for the round.  If not continuous,
        stopping when dealer has completed their turn.
        Returns -1 if the round has finished."""
        if self.round_clockwise:
            self.round_next_player += 1
        else:
            self.round_next_player -= 1
        self.round_next_player %= len(self.players)
        if self.round_one_shot and \
                self.round_start_player == self.round_next_player:
            self.round_next_player = -1
        # print("Get next round: player", self.round_next_player,
        #      "one_shot", self.round_one_shot,
        #      "clockwise", self.round_clockwise)
        return self.round_next_player


class Deck(Pile):
    """An empty deck with common methods."""

    def __init__(self, name="Deck"):
        Pile.__init__(self, name)

    def shuffle(self):
        """Shuffles the cards in the deck by swapping them."""
        import random
        num_cards = self.count()
        for dummy in range(1, 3):
            for i in range(num_cards):
                j = random.randrange(i, num_cards)
                self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def deal(self, players, num_cards=999):
        """Deals num_cards to each hand in hands."""
        for dummy in range(0, num_cards):
            for player_num in range(len(players)):
                if self.is_empty():
                    break
                player = players.get_player(player_num)
                card = self.pop()
                player.hand.push(card)
                players.set_player(player_num, player)


class Deck52Card(Deck):
    """The commonly used 52 card deck."""

    def __init__(self, name="Deck"):
        Deck.__init__(self, name)
        for suit in Suit:
            for rank in Rank:
                if (Suit.Hearts < suit < Suit.Red) \
                        and (Rank.Ace < rank < Rank.Joker):
                    self.cards.append(Card(suit, rank))


class CardGame():
    """Creates the deck and shuffles it."""

    def __init__(self):
        deck = Deck()
        deck.shuffle()
