from colorama import Fore


class HeroInfo:

    def __init__(self):

        print("Initializing HeroInfo...")

        # Initialize a dictionary to hold the counts
        self.action_counts      = {}
        self.recent_actions     = {}  # Dictionary to store recent actions

        self.recent_strategies      = []
        self.recent_tactics         = []

        self.valid_roles        = ['BTN', 'UTG', 'BB', 'SB', 'HJ', 'MP', 'CO']
        self.valid_stages       = ['Pre-Flop', 'Flop', 'Turn', 'River']

       # The total number of betting opportunities where the Hero could bet or raise.
        self.total_betting_opportunities = 0

        # The total number of times the Hero has bluffed.
        self.total_bluffs = 0

        # The total number of opportunities the Hero had to play pre-flop (excluding the blinds).
        self.total_preflop_opportunities = 0

        # The total number of times the Hero has folded pre-flop.
        self.total_preflop_folds = 0

        # The total number of times the Hero has bet or raised (aggressive actions).
        self.total_bets_and_raises = 0

        # The total number of times the Hero has called (passive action).
        self.total_calls = 0

        # The total number of hands played.
        self.total_hands = 0

        # The total number of hands where the Hero put money in the pot voluntarily.
        self.total_vpip_hands = 0

        # The total number of hands where the Hero has raised pre-flop.
        self.total_pfr_hands = 0

        # The total number of opportunities the Hero had to make a continuation bet post-flop.
        self.total_cbet_opportunities = 0

        # The total number of times the Hero made a continuation bet post-flop.
        self.total_cbets_made = 0

        # The total number of hands where the Hero went to showdown.
        self.total_hands_went_to_showdown = 0

        # The total number of opportunities the Hero had to 3-bet pre-flop.
        self.total_3bet_opportunities = 0

        # The total number of times the Hero made a 3-bet pre-flop.
        self.total_3bets = 0

        # The total number of times the Hero folded to a 3-bet after making an initial raise.
        self.total_folds_to_3bet = 0

        # The total number of times the Hero attempted to steal the blinds.
        self.total_steal_attempts = 0

        # The total number of opportunities the Hero had to attempt a steal from late positions.
        self.total_steal_opportunities = 0

        # The total number of bluff attempts made by the Hero.
        self.total_bluff_attempts = 0

        # The total number of successful bluff attempts made by the Hero.
        self.total_successful_bluffs = 0

        # The total number of pots won by the Hero.
        self.total_pots_won = 0

        # The total amount of winnings accumulated by the Hero.
        self.total_winnings = 0

        print("HeroInfo initialized!")


    def add_strategy(self, strategy):
        """
        Add a strategy to the list of recent strategies.
        strategy: The strategy to add.
        """
        self.recent_strategies.append(strategy)

    def add_tactic(self, tactic):
        """
        Add a tactic to the list of recent tactics.
        tactic: The tactic to add.
        """
        self.recent_tactics.append(tactic)

    def get_recent_strategies(self):
        """
        Retrieve and format the 15 most recent strategies.
        :return: A string representing the 15 most recent strategies.
        """
        return ', '.join(self.recent_strategies[-15:])

    def get_recent_tactics(self):
        """
        Retrieve and format the 15 most recent tactics.
        :return: A string representing the 15 most recent tactics.
        """
        return ', '.join(self.recent_tactics[-15:])
    

    def update_action_count(self, round_number, hero_role, board_stage, hero_action):
        """
        Update the count of actions based on the hero's role, board stage, action, and round number.
        Validates the role, stage, and round number before updating.
        hero_role: The role of the hero (e.g., 'BTN', 'UTG', 'BB', 'SB', 'HJ', 'MP', 'CO').
        board_stage: The stage of the board (e.g., 'Pre-flop', 'Flop', 'Turn', 'River').
        hero_action: The action taken by the hero (e.g., 'Fold', 'Check', 'Raise', 'Bet', 'Cash Out', 'Resume').
        round_number: The round number of the game.
        """

        # Validate the role and stage
        if hero_role not in self.valid_roles:
            print(f"{Fore.RED}Invalid role: {hero_role}{Fore.RESET}")
            return
        
        if board_stage not in self.valid_stages:
            print(f"{Fore.RED}Invalid board stage: {board_stage}{Fore.RESET}")
            return

        # Initialize the role, stage, and round number in the dictionary if not present
        if hero_role not in self.action_counts:
            self.action_counts[hero_role] = {}

        if board_stage not in self.action_counts[hero_role]:
            self.action_counts[hero_role][board_stage] = {'Fold': 0, 'Check': 0, 'Call': 0, 'Raise': 0, 'Bet': 0, 'Cash Out': 0, 'Resume': 0}

        # Increment the action count
        if hero_action in self.action_counts[hero_role][board_stage]:
            self.action_counts[hero_role][board_stage][hero_action] += 1
        else:
            print(f"{Fore.RED}Unknown action: {hero_action}{Fore.RESET}")

        # Update recent actions
        if round_number not in self.recent_actions:
            self.recent_actions[round_number] = []

        # Append the new action along with the hero role and board stage
        self.recent_actions[round_number].append((hero_role, board_stage, hero_action))


    
    def get_recent_actions(self):
        """
        Returns a formatted string listing all recent actions in chronological order for the past 10 rounds.
        Actions are aggregated by round and stage.
        """

        # Check if recent_actions is empty
        if not any(self.recent_actions.values()):
            return "No recent actions available"

        # Format the output
        output = ""
        for round_number in sorted(self.recent_actions.keys())[-10:]:
            stages = {'Pre-Flop': [], 'Flop': [], 'Turn': [], 'River': []}

            # Aggregate actions by stage
            for hero_role, board_stage, hero_action in self.recent_actions[round_number]:
                stages[board_stage].append(hero_action)


            # Generate the output string for this round
            round_actions = []
            for stage, actions in stages.items():
                if actions:
                    actions_str = ', '.join(actions)
                    round_actions.append(f"{stage}: {actions_str}")

            if round_actions:
                round_actions_str = ', '.join(round_actions)
                output += f"Round {round_number}: {round_actions_str}\n"

        return output










    



    # TOTAL STATS COUNT
            
    def total_bets(self):
        """Calculate the total number of bets."""
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Bet', 0)
                   for role in self.action_counts
                   for stage in self.action_counts.get(role, {}))

    def total_raises(self):
        """Calculate the total number of raises."""
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Raise', 0)
                   for role in self.action_counts
                   for stage in self.action_counts.get(role, {}))

    def total_checks(self):
        """Calculate the total number of checks."""
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Check', 0)
                   for role in self.action_counts
                   for stage in self.action_counts.get(role, {}))

    def total_folds(self):
        """Calculate the total number of folds."""
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Fold', 0)
                   for role in self.action_counts
                   for stage in self.action_counts.get(role, {}))


    # PRE-FLOP STATS COUNT

    def total_folds_preflop(self):
        """Calculate the total number of folds in the pre-flop stage."""
        return sum(self.action_counts.get(role, {}).get('Pre-Flop', {}).get('Fold', 0) 
                   for role in self.action_counts)

    def total_raises_preflop(self):
        """Calculate the total number of raises in the pre-flop stage."""
        return sum(self.action_counts.get(role, {}).get('Pre-Flop', {}).get('Raise', 0) 
                   for role in self.action_counts)

    def total_calls_preflop(self):
        """Calculate the total number of calls in the pre-flop stage."""
        return sum(self.action_counts.get(role, {}).get('Pre-Flop', {}).get('Call', 0) 
                   for role in self.action_counts)
    


    #POST FLOP STATS COUNT

    def total_folds_postflop(self):
        """Calculate the total number of folds post-flop."""

        post_flop_stages = ['Flop', 'Turn', 'River']
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Fold', 0)
                   for role in self.action_counts
                   for stage in post_flop_stages if stage in self.action_counts.get(role, {}))

    def total_bets_postflop(self):
        """Calculate the total number of bets post-flop."""

        post_flop_stages = ['Flop', 'Turn', 'River']
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Bet', 0)
                   for role in self.action_counts
                   for stage in post_flop_stages if stage in self.action_counts.get(role, {}))

    def total_raises_postflop(self):
        """Calculate the total number of raises post-flop."""

        post_flop_stages = ['Flop', 'Turn', 'River']
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Raise', 0)
                   for role in self.action_counts
                   for stage in post_flop_stages if stage in self.action_counts.get(role, {}))

    def total_calls_postflop(self):
        """Calculate the total number of calls post-flop."""

        post_flop_stages = ['Flop', 'Turn', 'River']
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Call', 0)
                   for role in self.action_counts
                   for stage in post_flop_stages if stage in self.action_counts.get(role, {}))

    def total_checks_postflop(self):
        """Calculate the total number of checks post-flop."""

        post_flop_stages = ['Flop', 'Turn', 'River']
        return sum(self.action_counts.get(role, {}).get(stage, {}).get('Check', 0)
                   for role in self.action_counts
                   for stage in post_flop_stages if stage in self.action_counts.get(role, {}))



    # BOARD STAGE: FLOP (3 Cards on table) STATS
    def total_folds_flop(self):
        """Calculate the total number of folds on the flop."""

        return sum(self.action_counts.get(role, {}).get('Flop', {}).get('Fold', 0)
                   for role in self.action_counts)

    def total_bets_flop(self):
        """Calculate the total number of bets on the flop."""

        return sum(self.action_counts.get(role, {}).get('Flop', {}).get('Bet', 0)
                   for role in self.action_counts)

    def total_raises_flop(self):
        """Calculate the total number of raises on the flop."""

        return sum(self.action_counts.get(role, {}).get('Flop', {}).get('Raise', 0)
                   for role in self.action_counts)

    def total_calls_flop(self):
        """Calculate the total number of calls on the flop."""

        return sum(self.action_counts.get(role, {}).get('Flop', {}).get('Call', 0)
                   for role in self.action_counts)

    def total_checks_flop(self):
        """Calculate the total number of checks on the flop."""

        return sum(self.action_counts.get(role, {}).get('Flop', {}).get('Check', 0)
                   for role in self.action_counts)



     # BOARD STAGE: TURN (4 Cards on table) STATS
    def total_folds_turn(self):
        """Calculate the total number of folds on the turn."""

        return sum(self.action_counts.get(role, {}).get('Turn', {}).get('Fold', 0)
                   for role in self.action_counts)

    def total_bets_turn(self):
        """Calculate the total number of bets on the turn."""

        return sum(self.action_counts.get(role, {}).get('Turn', {}).get('Bet', 0)
                   for role in self.action_counts)

    def total_raises_turn(self):
        """Calculate the total number of raises on the turn."""

        return sum(self.action_counts.get(role, {}).get('Turn', {}).get('Raise', 0)
                   for role in self.action_counts)

    def total_calls_turn(self):
        """Calculate the total number of calls on the turn."""

        return sum(self.action_counts.get(role, {}).get('Turn', {}).get('Call', 0)
                   for role in self.action_counts)

    def total_checks_turn(self):
        """Calculate the total number of checks on the turn."""

        return sum(self.action_counts.get(role, {}).get('Turn', {}).get('Check', 0)
                   for role in self.action_counts)



     # BOARD STAGE: RIVER (5 Cards on table) STATS
    def total_folds_river(self):
        """Calculate the total number of folds on the river."""
        return sum(self.action_counts.get(role, {}).get('River', {}).get('Fold', 0)
                   for role in self.action_counts)

    def total_bets_river(self):
        """Calculate the total number of bets on the river."""
        return sum(self.action_counts.get(role, {}).get('River', {}).get('Bet', 0)
                   for role in self.action_counts)

    def total_raises_river(self):
        """Calculate the total number of raises on the river."""
        return sum(self.action_counts.get(role, {}).get('River', {}).get('Raise', 0)
                   for role in self.action_counts)

    def total_calls_river(self):
        """Calculate the total number of calls on the river."""
        return sum(self.action_counts.get(role, {}).get('River', {}).get('Call', 0)
                   for role in self.action_counts)

    def total_checks_river(self):
        """Calculate the total number of checks on the river."""
        return sum(self.action_counts.get(role, {}).get('River', {}).get('Check', 0)
                   for role in self.action_counts)
    
    #Update the number of times the Hero had an opportunity to Bet *TODO*
    def update_betting_opportunity_count(self):
            self.total_betting_opportunities += 1



    def calculate_stack_to_pot_ratio( self, stack_size, pot_size ):
        """
        Calculate the Stack-to-Pot Ratio (SPR).

        :param stack_size: The size of the player's stack.
        :param pot_size: The current size of the pot.
        :return: The SPR value.
        """
        if pot_size == 0:
            return float('inf')  # To handle division by zero if the pot size is 0
        
        return stack_size / pot_size




    def update_bluff_stats(self, was_betting_opportunity, was_bluff):

        if was_betting_opportunity:
            self.total_betting_opportunities += 1

            if was_bluff:
                self.total_bluffs += 1



    def update_preflop_stats(self, had_opportunity, did_fold):

        if had_opportunity:
            self.total_preflop_opportunities += 1

            if did_fold:
                self.total_preflop_folds += 1



    def calculate_bluffing_frequency(self):

        if self.total_betting_opportunities == 0:
            return 0
        return self.total_bluffs / self.total_betting_opportunities



    def calculate_preflop_folding_frequency(self):

        if self.total_preflop_opportunities == 0:
            return 0 
        return self.total_preflop_folds / self.total_preflop_opportunities



    def calculate_pot_odds(self, call_amount, total_pot):
        """
        Calculate the pot odds.
        """
        if call_amount == 0:
            return float('inf')  # Avoid division by zero
        return total_pot / call_amount



    def update_aggression_stats(self, action):
        """
        Update the aggression statistics based on the Hero's action.
        """

        if action in ['Bet', 'Raise']:
            self.total_bets_and_raises += 1
        elif action == 'Calls':
            self.total_calls += 1


    #VPIP (Voluntarily Put Money In Pot):
    def calculate_aggression_factor(self):
        """
        Calculate the Hero's aggression factor.
        """
        if self.total_calls == 0:
            return float('inf') if self.total_bets_and_raises > 0 else 0
        return self.total_bets_and_raises / self.total_calls


    #PFR (Pre-Flop Raise):
    def update_vpip_pfr_stats(self, did_vpip, did_pfr):
        """
        Calculate the percentage of hands in which the Hero raises pre-flop.
        This provides insights into how aggressive the Hero is playing pre-flop.
        """
        self.total_hands += 1
        if did_vpip:
            self.total_vpip_hands += 1
        if did_pfr:
            self.total_pfr_hands += 1

    #CBet (Continuation Bet) Frequency:
    def update_cbet_stats(self, had_opportunity, did_cbet):
        """
        Calculate the percentage of hands in which the Hero voluntarily puts money into the pot pre-flop (excluding the blinds).
        This metric gives an indication of how often the Hero is playing hands.
        """
        if had_opportunity:
            self.total_cbet_opportunities += 1
            if did_cbet:
                self.total_cbets_made += 1

    #WTSD (Went to Showdown):
    def update_wtsd_stats(self, went_to_showdown):
        """
        Calculate the percentage of hands where the Hero sees the showdown after seeing the flop.
        This can indicate how often the Hero stays in a hand until the end.
        """
        if went_to_showdown:
            self.total_hands_went_to_showdown += 1


    def calculate_vpip(self):
        return (self.total_vpip_hands / self.total_hands) * 100 if self.total_hands > 0 else 0


    def calculate_pfr(self):
        return (self.total_pfr_hands / self.total_hands) * 100 if self.total_hands > 0 else 0


    def calculate_cbet_frequency(self):
        return (self.total_cbets_made / self.total_cbet_opportunities) * 100 if self.total_cbet_opportunities > 0 else 0


    def calculate_wtsd(self):
        return (self.total_hands_went_to_showdown / self.total_hands) * 100 if self.total_hands > 0 else 0



    #3-Bet Frequency:
    def update_3bet_stats(self, had_opportunity, did_3bet):
        """
        Measure how often the Hero re-raises pre-flop after an initial raise has been made.
        This indicates the Hero's aggression and adaptability in pre-flop play.
        """
        if had_opportunity:
            self.total_3bet_opportunities += 1
            if did_3bet:
                self.total_3bets += 1

    #Fold to 3-Bet Frequency:
    def update_fold_to_3bet_stats(self, faced_3bet, did_fold):
        """
        Track how often the Hero folds to a 3-bet after they have made an initial raise.
        This helps in understanding how the Hero responds to aggression from others.
        """
        if faced_3bet:
            self.total_folds_to_3bet += 1 if did_fold else 0

    #Steal Attempt Frequency:
    def update_steal_attempt_stats(self, in_steal_position, attempted_steal):
        """
        Calculate how often the Hero attempts to steal the blinds from late positions (cutoff, button, small blind).
        This statistic is useful for assessing how the Hero exploits positional advantages.
        """
        if in_steal_position:
            self.total_steal_opportunities += 1
            if attempted_steal:
                self.total_steal_attempts += 1

    def calculate_3bet_frequency(self):
        return (self.total_3bets / self.total_3bet_opportunities) * 100 if self.total_3bet_opportunities > 0 else 0

    def calculate_fold_to_3bet_frequency(self):
        return (self.total_folds_to_3bet / self.total_3bet_opportunities) * 100 if self.total_3bet_opportunities > 0 else 0

    def calculate_steal_attempt_frequency(self):
        return (self.total_steal_attempts / self.total_steal_opportunities) * 100 if self.total_steal_opportunities > 0 else 0





    def update_bluff_stats(self, attempted_bluff, was_successful):
        """
        Update the statistics for the Hero's bluff attempts.
        :param attempted_bluff: Indicates if a bluff was attempted.
        :param was_successful: Indicates if the bluff attempt was successful.
        """
        if attempted_bluff:
            self.total_bluff_attempts += 1
            if was_successful:
                self.total_successful_bluffs += 1

    def update_winnings_stats(self, won_pot, pot_size):
        """
        Update the statistics for the Hero's winnings.
        :param won_pot: Indicates if the Hero won the pot.
        :param pot_size: The size of the pot won by the Hero.
        """
        if won_pot:
            self.total_pots_won += 1
            self.total_winnings += pot_size

    def calculate_bluff_success_rate(self):
        """
        Calculate the success rate of the Hero's bluffs.
        """
        if self.total_bluff_attempts == 0:
            return 0
        return (self.total_successful_bluffs / self.total_bluff_attempts) * 100

    def calculate_average_pot_size_won(self):
        """
        Calculate the average size of the pots won by the Hero.
        """
        if self.total_pots_won == 0:
            return 0
        return self.total_winnings / self.total_pots_won
