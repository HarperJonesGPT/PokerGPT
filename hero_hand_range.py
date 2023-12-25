class PokerHandRangeDetector:

    def __init__(self):
        print("PokerHandRangeDetector Initialized..")


    def is_hand_in_range(self, hero_cards):
        """
        Check if the given hand contains a pair or an Ace, King, Queen, or Jack.

        hero_cards: A list of cards representing the hand (e.g., ['Q♠', 'Q♦']).
        
        :return: True if the hand contains a pair or any of these high cards, False otherwise.
        """
        # Mapping for card ranks, including '10'
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        # Extract ranks using the helper method
        rank1, _ = self.extract_rank_and_suit(hero_cards[0])
        rank2, _ = self.extract_rank_and_suit(hero_cards[1])

        # Normalize ranks to numerical values for comparison
        rank1_value = rank_values[rank1]
        rank2_value = rank_values[rank2]

        # Check for a pair (same numerical rank values) 
        # or high cards (Ace, King, Queen, Jack)
        if rank1_value == rank2_value or rank1 in ['A', 'K', 'Q', 'J'] or rank2 in ['A', 'K', 'Q', 'J']:
            return True
        else:
            return False


    def extract_rank_and_suit(self, card):
        """
        Extract rank and suit from a card string.
        Handles the '10' rank correctly.
        """
        if card.startswith('10'):
            return '10', card[2]
        else:
            return card[0], card[1]