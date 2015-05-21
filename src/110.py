'''
Created on 19 May 2015

@author: andy
'''

# Scores

import CardGame


class Player110(CardGame.Player):
    """The deck for 110 is a normal deck with one joker."""

    def __init__(self, name=""):
        self.current_score = 0
        self.name = name


class Deck110(CardGame.Deck):
    """The deck for 110 is a normal deck with one joker."""

    def __init__(self, name="Deck"):
        CardGame.Deck.__init__(self, name)
        self.cards.append(CardGame.Card(CardGame.Suit.Red,
                                        CardGame.Rank.Joker))


class CardGame110():
    """Plays the game of 110."""

    def __init__(self, num_players):
        self.deck = Deck110()
        self.deck.shuffle()
        for i in range(0, 4):
            self.players[i] = Player110("Player" + i)

    def DealHands(self):
        """Deals 5 cards to each player."""
        self.deck.deal(self.players, 5)

    def Bid(self):
        """ ."""

    def ExchangeCards(self):
        """ ."""

    def PlayHand(self):
        """ ."""

    def UpdateScores(self):
        """ ."""

    def ResetScores(self):
        """ ."""

    def PlayAgain(self):
        """ ."""
        return False

    def TerminateGame(self):
        """ ."""

    def Play(self):
        """ ."""
        play_again = True
        while play_again:
            # Zero current scores
            highest_current_score = 0
            while highest_current_score < 110:
                self.DealHands()
                self.Bid()
                self.ExchangeCards()
                self.PlayHand()
                highest_current_score = self.UpdateScores()
            play_again = self.PlayAgain()
            self.TerminateGame()


if __name__ == '__main__':
    CardGame110.Play()
