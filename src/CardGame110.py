'''
Created on 19 May 2015

@author: andy
'''

# Scores

import CardGame


class Card110(CardGame.Card):
    """The 110 version of a card with a different value method """

    def value(self, trump_suit):
        """Returns the value of the card. The value rules for 110 are:
        5 Hearts
        Jack of trumps
        Joker
        Trump suit in order
        All other suits in order
        The order of the suits is different for Red and Black suits.
        Red is 'normal', Ace, King, Queen, Jack, 10 to 2.
        Black is 'lowest in black', Ace, King, Queen, Jack, 2 to 10.
        The value is only used for comparison.
        Non trump Black and Red cards have the same values.
        Trump values are always greater than the cards of non-trump suit."""
        value = int(0)
        if self.rank == CardGame.Rank.Five and \
                self.suit == CardGame.Suit.Hearts:
            value = 50
        elif self.rank == CardGame.Rank.Jack and self.suit == trump_suit:
            value = 48
        elif self.rank == CardGame.Rank.Joker:
            value = 46
        elif self.suit == trump_suit:
            value = self.value_black_and_red() + 20
        else:
            value = self.value_black_and_red()
        return value

    def value_black_and_red(self):
        """Value the card for the black and red suits.
        Only to be called from value."""
        value = int(0)
        if self.is_red():
            if CardGame.Rank.Ace == self.rank:
                value = 14
            else:
                value = int(self.rank)
        else:
            if CardGame.Rank.Ace == self.rank:
                value = 14
            else:
                value = int(self.rank)
                if value <= 10:
                    value = 11 - value
        return value


class Player110(CardGame.Player):
    """The player is a normal player with a current score."""

    def __init__(self, name=""):
        CardGame.Player.__init__(self, name)
        self.current_score = 0

    def reset(self):
        """Resets the player to defaults."""
        self.current_score = 0
        self.clear()


class Deck110(CardGame.Deck):
    """The deck for 110 is a normal deck with one joker."""

    def __init__(self):
        CardGame.Deck.__init__(self)
        for suit in CardGame.Suit:
            for rank in CardGame.Rank:
                if (CardGame.Suit.Hearts < suit < CardGame.Suit.Red) \
                        and (CardGame.Rank.Ace < rank < CardGame.Rank.Joker):
                    self.cards.append(Card110(suit, rank))
        self.cards.append(Card110(CardGame.Suit.Red,
                                  CardGame.Rank.Joker))


class CardGame110():
    """Plays the game of 110."""

    def __init__(self):
        self.deck = Deck110()
        self.highest_score = 0
        self.players = CardGame.Players()
        self.trump_suit = CardGame.Suit.Undefined

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

    def set_trump_suit(self, winning_bid_player_num):
        """The player who wins the bid selects the trump suit."""
        player = self.players.get_player(winning_bid_player_num)
        valid_card = False
        while not valid_card:
            trump_card = self.select_card_from_hand(
                player, "Select card for trump suit, 1-5 ")
            if trump_card.suit == CardGame.Suit.Undefined:
                valid_card = True
            print(player.hand.name, "selected", trump_card.suit)
        self.trump_suit = trump_card.suit

    def mark_cards_for_discard(self, player):
        """Mark the cards in the players hand that will be discarded."""
        cards_to_discard = [False, False, False, False, False]
        discarding = True
        while discarding:
            # Display cards with those marked for discard
            print("Player", player.hand.name, "Trump suit", self.trump_suit)
            print("Index  Discard  Card")
            for card_index in range(0, len(player.hand.cards)):
                print("{:5}  {:7}  {}".
                      format(str(card_index + 1),
                             str(cards_to_discard[card_index]),
                             str(player.hand.cards[card_index])))
            discard_string = input(
                "Enter card to discard, 1-5. Enter 0 when done.")
            try:
                discard_value = int(discard_string)
            except ValueError:
                discard_value = -1
            if 0 < discard_value < 6:
                cards_to_discard[discard_value - 1] = \
                    not cards_to_discard[discard_value - 1]
            if discard_value == 0:
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
            print("Exchanged ", len(cards_to_discard), "cards")
            # Update the player's cards
            self.players.set_player(player_num, player)
            player_num = self.players.get_next_player_num_for_round()

    def select_card_from_hand(self, player, text_to_show):
        """Select the card in the players hand to be played."""
        # Display cards with those marked for discard
        print("Player " + player.hand.name, "Trump suit", self.trump_suit)
        print("Index  Card")
        card_index = 0
        selected_card = CardGame.Card()
        selected_card.rank = CardGame.Rank.Undefined
        for card_index in range(0, len(player.hand.cards)):
            print("{:5}  {}".
                  format(str(card_index + 1),
                         str(player.hand.cards[card_index])))
        play_string = input(text_to_show)
        try:
            play_value = int(play_string)
        except ValueError:
            play_value = -1
        # print("Selected value ", play_value)
        if 0 < play_value < len(player.hand.cards):
            selected_card = player.hand.cards[play_value - 1]
        return selected_card

    def play_trick(self, starting_player_num):
        """Play one card from each player in turn.  Determines the winning
        player and the value of the winning trick."""
        print("Play round")
        winning_score = -1
        winning_player_num = -1
        suit_to_follow = CardGame.Suit.Undefined
        first_player = False
        invalid_card_played = True
        player_num = self.players.start_round(starting_player_num)
        while player_num is not -1:
            player = self.players.get_player(player_num)
            while invalid_card_played:
                card_to_play = self.select_card_from_hand(
                    player, "Select card to play, 1-5 ")
                print(player.hand.name, " played the ", card_to_play)
                # Check to make sure the player has followed suit correctly.
                invalid_card_played = False
                if not first_player:
                    first_player = True
                    suit_to_follow = card_to_play.suit
                else:
                    if suit_to_follow != card_to_play.suit:
                        for card_index in range(0, len(player.hand.cards)):
                            if player.hand.cards[card_index].suit == \
                                    suit_to_follow:
                                invalid_card_played = True
                                print("You must follow suit!!!!")
            value = card_to_play.value(self.trump_suit)
            if winning_score < value:
                winning_score = value
                winning_player_num = player_num
            player_num = self.players.get_next_player_num_for_round()
        return (winning_score, winning_player_num)

    def play_hand(self, starting_player_num):
        """Play all cards in hand by playing one round at a time.
        Each trick scores the winner 5 points.  The player that has the
        highest value trick at the end of the hand gets a 5 point bonus."""
        print("Play hand")
        highest_score = -1
        highest_scoring_player_num = -1
        player_num = self.players.start_round(starting_player_num)
        while player_num is not -1:
            winning_score, winning_player_num = \
                self.play_trick(starting_player_num)
            if highest_score < winning_score:
                highest_score = winning_score
                highest_scoring_player_num = winning_player_num
            # Update the scores for the trick.
            winning_player = self.players.get_player(winning_player_num)
            winning_player.current_score += 5
            self.players.set_player(winning_player_num, winning_player)
            player_num = self.players.get_next_player_num_for_round()
        # Score the 5 point bonus
        highest_scoring_player = \
            self.players.get_player(highest_scoring_player_num)
        highest_scoring_player.current_score += 5
        self.players.set_player(highest_scoring_player_num,
                                highest_scoring_player)

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
        """Play a round."""
        play_again = True
        while play_again:
            # Zero current scores
            self.reset_scores()
            winning_player_num = -1
            while winning_player_num == -1:
                self.deck.shuffle()
                self.deal_hands()
                starting_player_num = self.bid()
                self.set_trump_suit(starting_player_num)
                player_num = self.players.start_round(starting_player_num)
                while player_num is not -1:
                    self.exchange_cards(starting_player_num)
                    self.play_hand(starting_player_num)
                    winning_player_num = self.update_scores(
                        starting_player_num)
                    player_num = self.players.get_next_player_num_for_round()
            input_string = input('Enter y to play again...')
            if input_string != "y":
                play_again = False


if __name__ == '__main__':
    GAME = CardGame110()
    GAME.add_players()
    GAME.play()
