"""
Created on 17 May 2015

@author: andy
"""


class Card:

    def __init__(self, suit=0, rank=0):
        if ((1 <= suit <= 4) and (1 <= rank <= 13)):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = 0
            self.rank = 0
            raise ValueError("Parameter out of range")
