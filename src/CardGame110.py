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
        self.is_dealer = False

    def reset(self):
        """Resets the player to defaults."""
        self.current_score = 0
        self.is_dealer = 0
        self.clear()


class Players110():
    """A list of player instances with the ability to add players and to
    iterate over the list of players in a circular fashion with a nominated
    player starting first."""

    def __init__(self):
        self.entry = 0
        self.players = list()

    def __len__(self):
        return len(self.players)

    def append(self, player):
        """Appends the player."""
        self.players.append(player)

    def clear(self):
        """Clears the list of players."""
        self.players.clear()

    def reset(self):
        """Reset each player to the default state."""
        for i in range(len(self.players)):
            self.players[i].reset()

    def get_player(self, player_num):
        """Returns a copy of the player with player_num."""
        return self.players[player_num]

    def set_player(self, player_num, new_player):
        """Overwrites the player with player_num."""
        self.players[player_num] = new_player

    def add_card_for_player(self, player_num, card):
        """Add card to player_num hand."""
        self.players[player_num].hand.add(card)

    def list_hand_for_player(self, player_num):
        """Print out hand for player_num."""
        self.players[player_num].hand.list()

    def get_name(self, player_num):
        """Get name of player. """
        return self.players[player_num].hand.name

    def is_dealer(self, player_num):
        """Get value of is_dealer for player. """
        return self.players[player_num].is_dealer


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
        self.players = Players110()
        for i in range(num_players):
            player = Player110("Player" + str(i))
            player.current_score = 0
            if i == 0:
                player.is_dealer = True
            self.players.append(player)

    def reset_scores(self):
        """ ."""
        print("Resetting scores and player's hands")
        self.highest_score = 0
        self.players.reset()

    def deal_hands(self):
        """Deals 5 cards to each player."""
        print("Dealing hand")
        self.deck.deal(self.players, 5)

    def bid(self):
        """The bidding phase of the game.  Starting with the player to the
        left of the dealer, each player bids for the right to chose the
        trump suit.  The bids must be either no bid or a minimum of 15 points
        and a maximum of 30 points.  The dealer has the bonus of winning the
        bid with a bid equal to the highest bid."""
        print("bidding")
        bidding_player = 0
        highest_bid = 10
        highest_bid_player = -1
        for player_num in range(0, len(self.players)):
            player = self.players.get_player(player_num)
            player.hand.list()
            bid_string = input("Enter bid, 0, 15, 20, 25, 30 ")
            try:
                bid_value = int(bid_string)
            except ValueError:
                bid_value = -1
            if bid_value >= 15 and bid_value <= 30 and (bid_value % 5) == 0:
                # Bid in range
                if bid_value > highest_bid:
                    highest_bid = bid_value
                    highest_bid_player = player_num
                    print(player.hand.name + " takes bid with "
                          + str(bid_value))
                if bid_value == highest_bid and \
                        self.players.is_dealer(player_num):
                    highest_bid_player = player_num
                    print("Dealer takes bid with " + bid_value)
            # Else bid out of range so treat as no bid.
        if highest_bid == 10:
            print("No bid from anyone.  Deal again.")
            return False
        return True

    def mark_cards_for_discard(self, player):
        """Mark the cards in the players hand that will be discarded."""
        cards_to_discard = [False, False, False, False, False]
        discarding = True
        while discarding:
            # Display cards with those marked for discard
            print("Player " + player.hand.name)
            print("Index  Discard  Card")
            for card_index in range(0, len(player.hand.cards)):
                print("{:5}  {:7}  {}".
                      format(str(card_index + 1),
                             str(cards_to_discard[card_index]),
                             str(player.hand.cards[card_index])))
            bid_string = input(
                "Enter card to discard, 1-5. Enter 0 when done.")
            try:
                bid_value = int(bid_string)
            except ValueError:
                bid_value = -1
            if 0 < bid_value < 6:
                cards_to_discard[bid_value - 1] = True
            if bid_value == 0:
                discarding = False
        return cards_to_discard

    def exchange_cards(self):
        """Each player in turn discards zero or more cards."""
        print("Exchange cards")
        for player_num in range(0, len(self.players)):
            player = self.players.get_player(player_num)
            cards_to_discard = self.mark_cards_for_discard(player)
            # Replace them with new cards from the deck.
            for card_index in range(0, len(player.hand.cards)):
                if cards_to_discard[card_index]:
                    player.hand.cards[card_index] = self.deck.pop()
            # Update the player's cards
            self.players.set_player(player_num, player)

    def play_hand(self):
        """ ."""
        print("play hand")
        for player_num in range(0, len(self.players)):
            player = self.players.get_player(player_num)
            # Debug
            player.hand.list()

    def update_scores(self):
        """ ."""
        print("Updating scores")
        # AJB Bodge
        player = self.players.get_player(0)
        player.current_score = 120
        self.players.set_player(0, player)
        # Update self.highest_score from players individual scores
        self.highest_score = 0
        for player_num in range(len(self.players)):
            player = self.players.get_player(player_num)
            print(player.hand.name + " has " +
                  str(player.current_score))
            if self.highest_score < player.current_score:
                self.highest_score = player.current_score

#    def terminate_game(self):
#        """ ."""

    def play(self):
        """play a round."""
        play_again = True
        while play_again:
            self.reset_scores()
            # Zero current scores
            while self.highest_score < 110:
                self.deal_hands()
                if self.bid():
                    self.exchange_cards()
                    self.play_hand()
                    self.update_scores()
            input_string = input('Enter y to play again...')
            if input_string != "y":
                play_again = False
#           self.terminate_game()


if __name__ == '__main__':
    GAME = CardGame110(4)
    GAME.play()
