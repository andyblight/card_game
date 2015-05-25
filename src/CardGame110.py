'''
Created on 19 May 2015

@author: andy
'''

# Scores

import CardGame


class Player110(CardGame.Player):
    """The player is a normal player with a current score."""

    def __init__(self, name=""):
        CardGame.Player.__init__(self, name)
        self.current_score = 0


class Deck110(CardGame.Deck):
    """The deck for 110 is a normal deck with one joker."""

    def __init__(self, name="Deck"):
        CardGame.Deck.__init__(self, name)
        self.cards.append(CardGame.Card(CardGame.Suit.Red,
                                        CardGame.Rank.Joker))


class CardGame110():
    """Plays the game of 110."""

    def __init__(self, num_players):
        # Create and shuffle the deck
        self.deck = Deck110()
        self.deck.shuffle()
        # Create highest score
        self.highest_score = 0
        # Create the players
        self.players = list()
        for i in range(0, 4):
            self.players.append(Player110("Player" + str(i)))

    def ResetScores(self):
        """ ."""
        print("Resetting scores and player's hands")
        self.highest_score = 0
        for i in range(len(self.players)):
            self.players[i].current_score = 0
            self.players[i].clear()

    def DealHands(self):
        """Deals 5 cards to each player."""
        print("Dealing hand")
        self.deck.deal(self.players, 5)

    def Bid(self):
        """ ."""
        print("Bidding")
        for i in range(len(self.players)):
            self.players[i].hand.list()

    def ExchangeCards(self):
        """ ."""
        print("Exchange cards")

    def PlayHand(self):
        """ ."""
        print("Play hand")

    def UpdateScores(self):
        """ ."""
        print("Updating scores")
        # AJB Bodge
        self.players[0].current_score = self.players[0].current_score + 120
        self.highest_score = 0
        for i in range(len(self.players)):
            print(self.players[i].hand.name + " has " +
                  str(self.players[i].current_score))
            if self.highest_score < self.players[i].current_score:
                self.highest_score = self.players[i].current_score

    def PlayAgain(self):
        """ ."""
        input_string = input('Enter y to play again...')
        if input_string == "y":
            return True
        else:
            return False

    def TerminateGame(self):
        """ ."""

    def Play(self):
        """Play a round."""
        play_again = True
        while play_again:
            self.ResetScores()
            # Zero current scores
            while self.highest_score < 110:
                self.DealHands()
                self.Bid()
                self.ExchangeCards()
                self.PlayHand()
                self.UpdateScores()
            play_again = self.PlayAgain()
            self.TerminateGame()


if __name__ == '__main__':
    game = CardGame110(4)
    game.Play()
