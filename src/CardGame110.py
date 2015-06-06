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

    def reset(self):
        """Resets the player to defaults."""
        self.current_score = 0
        self.clear()


class Deck110(CardGame.Deck52Card):
    """The deck for 110 is a normal deck with one joker."""

    def __init__(self):
        CardGame.Deck52Card.__init__(self)
        self.cards.append(CardGame.Card(CardGame.Suit.Red,
                                        CardGame.Rank.Joker))


class CardGame110():
    """Plays the game of 110."""

    def __init__(self):
        self.deck = Deck110()
        self.highest_score = 0
        self.players = CardGame.Players()

    def add_players(self):
        """For now, this is a bodge so just add four players."""
        self.players.clear()
        player = Player110("Andy")
        player.is_dealer = True
        self.players.append(player)
        player = Player110("Brian")
        self.players.append(player)
        player = Player110("Colin")
        self.players.append(player)
        player = Player110("David")
        self.players.append(player)

    def reset_scores(self):
        """ ."""
        print("Resetting scores and player's hands")
        self.highest_score = 0
        self.players.reset()

    def deal_hands(self):
        """Deals 5 cards to each player."""
        num_cards = 5
        print("Dealing", num_cards, "cards to",
              len(self.players), "players")
        self.deck.deal(self.players, num_cards)

    def bid(self):
        """The bidding phase of the game.
        Starting with the player to the left of the dealer, each player bids
        for the right to chose the trump suit.  The bids must be either no
        bid or a minimum of 15 points and a maximum of 30 points.  The dealer
        has the bonus of winning the bid with a bid equal to the current
        highest bid.
        The bidding is complete when either a bid of 30 is called or refused
        by the dealer or the when the highest, non-maximum bid is refused by
        all players after the player with the current highest bid.
        Returns the player number with the winning bid."""
        print("Bidding round")
        winning_bid = 10
        winning_bid_player = -1
        starting_player_num = self.players.get_player_num_left_of_dealer()
        player_num = self.players.start_round(starting_player_num, False)
        while player_num is not -1:
            if player_num is winning_bid_player:
                # Gone round with no takers so bidding over
                break
            player = self.players.get_player(player_num)
            player.hand.list()
            bid_string = input("Enter bid, 0, 15, 20, 25, 30 ")
            try:
                bid_value = int(bid_string)
            except ValueError:
                bid_value = -1
            if bid_value >= 15 and bid_value <= 30 and (bid_value % 5) == 0:
                # Bid in range
                if bid_value > winning_bid:
                    winning_bid = bid_value
                    winning_bid_player = player_num
                    print(
                        player.hand.name + " takes bid with " + str(bid_value))
                if player.is_dealer:
                    if bid_value == winning_bid:
                        winning_bid_player = player_num
                        print("Dealer takes bid with " + bid_value)
                    if bid_value == 30:
                        # Maximum bid and player is dealer so bidding over
                        break
            # Else bid out of range so treat as no bid.
            player_num = self.players.get_next_player_num_for_round()
        if winning_bid == 10:
            print("No bid from anyone.  Deal again.")
            winning_bid_player = -1
        return winning_bid_player

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

    def exchange_cards(self, starting_player_num):
        """Each player in turn discards zero or more cards."""
        print("Exchange cards")
        player_num = self.players.start_round(starting_player_num)
        while player_num is not -1:
            player = self.players.get_player(player_num)
            cards_to_discard = self.mark_cards_for_discard(player)
            # Replace them with new cards from the deck.
            for card_index in range(0, len(player.hand.cards)):
                if cards_to_discard[card_index]:
                    player.hand.cards[card_index] = self.deck.pop()
            # Update the player's cards
            self.players.set_player(player_num, player)
            player_num = self.players.get_next_player_num_for_round()

    def play_hand(self, starting_player_num):
        """ ."""
        print("play hand")
        player_num = self.players.start_round(starting_player_num)
        while player_num is not -1:
            player = self.players.get_player(player_num)
            # Debug
            player.hand.list()
            player_num = self.players.get_next_player_num_for_round()

    def update_scores(self, starting_player_num):
        """ ."""
        print("Updating scores")
        # AJB Bodge
        player = self.players.get_player(0)
        player.current_score = 120
        self.players.set_player(0, player)
        # Update self.highest_score from players individual scores
        self.highest_score = 0
        winning_player = -1
        player_num = self.players.start_round(starting_player_num)
        while player_num is not -1:
            player = self.players.get_player(player_num)
            if self.highest_score < player.current_score:
                self.highest_score = player.current_score
            # The first player to score 110 wins the game
            if self.highest_score >= 110:
                winning_player = player_num
                print(
                    player.hand.name + " has won the game with a score of " +
                    str(player.current_score))
                break
            else:
                print(player.hand.name + " has a score" +
                      str(player.current_score))
            player_num = self.players.get_next_player_num_for_round()
        return winning_player

    def play(self):
        """play a round."""
        play_again = True
        while play_again:
            # Zero current scores
            self.reset_scores()
            winning_player_num = -1
            while winning_player_num == -1:
                self.deal_hands()
                starting_player_num = self.bid()
                if starting_player_num is not -1:
                    self.exchange_cards(starting_player_num)
                    self.play_hand(starting_player_num)
                    winning_player_num = self.update_scores(
                        starting_player_num)
            input_string = input('Enter y to play again...')
            if input_string != "y":
                play_again = False


if __name__ == '__main__':
    GAME = CardGame110()
    GAME.add_players()
    GAME.play()
