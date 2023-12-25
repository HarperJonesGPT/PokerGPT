import datetime
import os
import time
import re
from colorama import Fore
import pygetwindow as gw

class GameState:

    def __init__( self, hero_action, audio_player ):

        self.hero_action        = hero_action

        self.audio_player       = audio_player


        self.log = []                                               # Initializing the log list

        self.all_round_logs = []                                    # Dictionary to store logs of each round

        self.last_round_end_time = time.time()                      # Initialize with the current time

        self.rounds_since_last_clear = 0                            # Keep track of resetting the round logs data

        self.players = {}                                           # All players data *DONE*

        self.active_players = [1,2,3,4,5,6]                          # List of active player numbers who are currently active in the game *DONE*

        self.hero_player_number = 0                                 # Player number for the Hero

        self.small_blind    = 0                                     # Small blind(SB) value calculated at beginning of the new round
        
        self.big_blind      = 0                                     # Big blind(BB) value calculated at beginning of the new round

        self.hero_total_hands_dealt = 0                             # Total hands health to hero player *TODO*

        self.hero_hands_played = 0                                  # Total hands played after pre-flop for hero player *TODO*

        self.community_cards = []                                   # List of community cards on community_cardshe table *DONE*

        self.hero_cards = []                                        # List of Heroplayer 1 cards *DONE*

        self.last_hero_action_log = ""                              # Last action of the hero with AI analysis(this is used for GUI display)

        self.hero_cards_combination = 'Unknown'                      # Herop player combination(Pairs, Flush etc.) *DONE*

        self.bluff_count = 0                                        # Keep track of bluffs for the hero (player1) *DONE*

        self.value_bet_count = 0                                    # Keep track of value bets for the Hero (player1) *DONE*


        self.dealer_position = -1                                   # Player number who is the current dealer. Default -1(none) *DONE*

        self.round_count = 0                                        # count the number of rounds played *DONE*

        self.current_board_stage = 'Pre-Flop'                       # Current stage of the game *DONE*

        self.total_pot = 0                                          # Total amount in the pot on table *DONE*

        self.betting_history = []                                   # History of all player hands *DONE*
 

    def extract_blinds_from_title(self):
        title_contains = "No Limit" 
        windows = gw.getWindowsWithTitle(title_contains)

        for window in windows:
            # Find all monetary amounts (assuming they follow a '$' symbol)
            amounts = re.findall(r'\$(\d+\.?\d*)', window.title)
            if amounts and len(amounts) >= 2:
                # Assuming the first amount is the small blind and the second is the big blind
                self.small_blind = float(amounts[0])
                self.big_blind = float(amounts[1])
                print(f"Small Blind: ${self.small_blind}, Big Blind: ${self.big_blind}")
                return True



    # Method to add an entry to the log
    def add_log_entry(self, data):
        final_string = ""
    
        # Update Turn
        if data.get('method') == 'update_player_turn':
            player_number   = data.get('player_number', 'N/A')

            if player_number == self.hero_player_number:
                final_string = f"Hero Turn"
            else:
                final_string = f"Player{player_number} Turn"


        # Update Cards
        elif data.get('method') == 'update_community_cards':
            board_stage = data['Stage']
            table_cards = data.get('Table Cards')

            # Joining the list elements with a space instead of a comma
            table_cards_str = '  '.join(table_cards) if table_cards else ''

            final_string = f"{board_stage}: {table_cards_str}" #Sample Output:  Flop: [Qh, 9d, 3s]
        

        # Update Cards
        elif data.get('method') == 'update_player_cards':
            player_number   = data.get('player_number', 'N/A')
            player_cards    = data.get('cards')

            player_cards_str = '  '.join(player_cards) if player_cards else ''

            if player_number == self.hero_player_number:
                final_string = f"Hero Cards: {player_cards_str}"
            else:
                final_string = f"Player{data['player_number']} Cards: {player_cards_str}"
           
        # Update Hero Actions
        elif data.get('method') == 'update_hero_action':

            action              = data.get('Action')
            amount              = data.get('Amount')
            action_tactic       = data.get('Tactic')
            action_strategy     = data.get('Strategy')
            action_explanation  = data.get('Explanation')

            # Convert amount to an integer
            try:
                amount = int(amount)
            except ValueError:
                # Handle the exception if amount is not a valid integer
                # For example, log an error message or set amount to 0
                amount = 0  # Or handle it in a way that makes sense for your application
 
            if amount > 0:
               final_string = (f"Hero Action: {action} ${amount} \n"
                        f"Tactic: {action_tactic}\n"
                        f"Strategy: {action_strategy}\n"
                        f"Explanation: {action_explanation}"
                        )
            else:
                final_string = (f"Hero Action: {action} \n"
                        f"Tactic: {action_tactic}\n"
                        f"Strategy: {action_strategy}\n"
                        f"Explanation: {action_explanation}"
                        )
                
            # Store the final_string in last_hero_action_log
            self.last_hero_action_log = final_string

        #Update Action Bet, Check, Fold, Call
        elif data.get('method') == 'update_player_action':
            player_number   = data.get('player_number', 'N/A')
            action          = data.get('action', 'None')
            time_seconds    = data.get('time', '0.1')
            role            = data.get('role', 'Unknown')

            if player_number == self.hero_player_number:
                final_string    = f"Hero({role}): {action} in {time_seconds} seconds"
            else:
                final_string    = f"Player{player_number}({role}): {action} in {time_seconds} seconds"

        #Update Action Raise + Amount
        elif data.get('method') == 'update_player_action_raise':
            player_number   = data.get('player_number', 'N/A')
            role            = data.get('role', 'Unknown')
            action          = data.get('action', 'Unknown')
            amount          = data.get('amount', '0')
            time_seconds    = float(data.get('time', '0.1'))
            pot_size        = data.get('pot_size', '0')

            time_str = ""
            if time_seconds == 0:
                time_str = ""
            else:
                time_str = f"in {time_seconds} seconds"

            if player_number == self.hero_player_number:
                if amount > 0:
                    final_string    = f"Hero({role}): {action} ${amount} {time_str} [Pot: ${pot_size}]" 
                else:
                    final_string    = f"Hero({role}): {action} {time_str} [Pot: ${pot_size}]" 
            else:
                if amount > 0:
                    final_string    = f"Player{player_number}({role}): {action} ${amount} {time_str} [Pot: ${pot_size}]" 
                else:
                    final_string    = f"Player{player_number}({role}): {action} {time_str} [Pot: ${pot_size}]"
            
            
        #Update Table pot size
        elif data.get('method') == 'update_total_pot':
            final_string    = f"Table Pot: ${data.get('Table Pot', 'N/A')}"
            
            
         #Update Blinds
        elif data.get('method') == 'update_blinds':
            small_blind   = data.get('small_blind', 'N/A')
            big_blind     = data.get('big_blind', 'N/A')

            final_string    = f"Small Blind(SB): ${small_blind} , Big Blind(BB): ${big_blind}"

        #Update Player Role
        elif data.get('method') == 'update_player_role':
            player_number   = data.get('player_number', 'N/A')
            role            = data.get('role', 'N/A')

            if player_number == self.hero_player_number:
                final_string    = f"Hero: {role}"
            else:
                final_string    = f"Player{player_number}: {role}"
            
           
        #Update Player hero
        elif data.get('method') == 'update_player_hero':
            player_number   = data.get('player_number', 'N/A')
            #hero            = data.get('hero', 'Unknown')
            final_string    = f"Player{player_number} is Hero"


        #Update All Players Stack sizes at the beginning of each round
        elif data.get('method') == 'update_players_stacks':
            player_number   = data.get('player_number', 'N/A')
            stack_size      = data.get('stack_size', 'N/A')
            role            = data.get('role')

            if player_number == self.hero_player_number:
                final_string    = f"Hero Stack({role}): ${stack_size}"
            else:
                final_string    = f"Player{player_number}({role}) Stack: ${stack_size}"


        #Update Player Status
        elif data.get('method') == 'update_player_status':
            player_number   = data.get('player_number', 'N/A')
            status          = data.get('status')
            final_string = f"Player{player_number}: {status}"


        #Update Player Won
        elif data.get('method') == 'update_player_won':
            player_number = data.get('player_number', 'N/A')
            won_amount = data.get('won_amount', '0')
            pots_won = data.get('pots_won', '0')

            if player_number == self.hero_player_number:
                final_string = f"Hero: Won ${won_amount}, Total Wins: {pots_won}"
            else:
                final_string = f"Player{player_number}: Won ${won_amount}, Total Wins: {pots_won}"


        #Update Total Players
        elif data.get('method') == 'update_total_players':
            final_string = f"Total Players: {len(self.active_players)}"

         #Update Round Count
        elif data.get('method') == 'reset_for_new_round':
            final_string = f"ROUND: {self.round_count}"

          #Update Round Count
        elif data.get('method') == 'hero_bluff_to_value_ratio':
            btf_ratio = data.get('bluff_value_ratio', '0')
            final_string = f"Hero Bluff-to-Value Ratio: {btf_ratio}"

        #Update New Round
        elif data.get('method') == 'line':
            final_string = f"----------------------------------"

        else:
            # Fallback for other types of data
            data_str = ', '.join([f"{key}: {value}" for key, value in data.items()])
            final_string = f"{data_str}"
        
        #print(final_string)
        
        self.log.append(final_string)
        self.all_round_logs.append(final_string)


    # Method to retrieve the log *DONE*
    def get_log(self):
        
        return self.log
    

    def get_ai_log(self):
        formatted_log = []
        for log_entry in self.log:
            # Splitting each entry by comma and removing extra spaces and quotes
            split_entries = log_entry.split(',')
            for entry in split_entries:
                cleaned_entry = entry.strip().replace("'", "")
                formatted_log.append(cleaned_entry)

        # Joining the entries with newline character for better readability
        return '\n'.join(formatted_log)
    


    def update_player(self, player_number, player_name=None, status=None, role=None, hero=None, cards=None, turn=None, action=None, amount=None, stack_size=None, won_amount=None, player_type=None, exploitation_strategy=None):
        """
        Update information about a specific player.
        """

        # Initialize player data if not already present
        if player_number not in self.players:
            self.players[player_number] = {
                'name': f'Player {player_number}',  # Correct
                'status':       'Active',  # Correct
                'role':         None,  # Correct
                'hero':         None,
                'cards':        None,  # Correct
                'turn':         None,  # Correct
                'turn_start_time': None,  # Correct
                'action':       None,   # Correct
                'action_time':  0.0,    # Correct
                'amount':       None,   # Correct
                'pot_size':     0.0,    # Correct
                'stack_size':   0.0,    # Correct
                'won_amount':   0.0,   # Correct
                'pots_won':     0,      # Correct
                'player_type':   None,   # Correct
                'exploitation_strategy':     None    # Correct
            }


        player_role = self.players.get(player_number, {}).get('role')
      
        # Update Player Name
        if player_name is not None:
            self.players[player_number]['name'] = player_name
            self.add_log_entry({'method': 'update_player_name','player_number': player_number, 'name': player_name })


        # Update Player Status
        if status is not None:
            self.players[player_number]['status'] = status

              # If the player's status is set to 'Active', add them to the active_players list
            if status == 'Active' and player_number not in self.active_players:
                self.active_players.append(player_number)
                #self.add_log_entry({'method': 'update_player_status','player_number': player_number, 'status': 'Active' })

            # If the player's status is set to 'Inactive', remove them from the active_players list
            elif status == 'Inactive' and player_number in self.active_players:
                self.active_players.remove(player_number)
                self.audio_player.play_left_audio(player_number)
                self.add_log_entry({'method': 'update_player_status','player_number': player_number, 'status': 'Inactive' })


        # Update Player Role (dealer, small blind, big blind)
        if role is not None:
            self.players[player_number]['role'] = role

            if role == "Dealer":
                self.audio_player.play_is_dealer_audio(player_number)


         # Update Hero Player number and name
        if hero is not None:
            self.players[player_number]['hero'] = True
            self.hero_player_number = player_number
            self.players[player_number]['name'] = f"Player{player_number} (Hero)"
            self.add_log_entry({'method': 'update_player_hero','player_number': player_number, 'hero': role })

        # Update Player Cards
        if cards is not None:
            self.players[player_number]['cards'] = cards
            self.add_log_entry({'method': 'update_player_cards','player_number': player_number,'cards': cards})


        # Update player turn
        if turn is not None:
            
            # Set all other players' turn to False if this player's turn is set to True
            if turn:
                for key in self.players:
                    if key != player_number:
                        self.players[key]['turn'] = False

                # Record start time when the turn is set to True
                self.players[player_number]['turn_start_time'] = time.time()
                #self.add_log_entry({'method': 'update_player_turn','player_number': player_number, 'turn': turn })
                #self.audio_player.play_turn_audio(player_number)
            else:
                # Reset turn start time when the turn is over
                self.players[player_number]['turn_start_time'] = None

            self.players[player_number]['turn'] = turn
                    

        # Update player action
        if action is not None:
            self.players[player_number]['action'] = action

            start_time = self.players.get(player_number, {}).get('turn_start_time')
            action_time = 0  

            if(start_time is not None):
                action_time = time.time() - self.players.get(player_number, {}).get('turn_start_time')
                action_time = round(action_time, 0)  # Round to one decimal place
                if action_time == 0: 
                    action_time = 1
                
             # Play corresponding audio based on action
            if action == "Bet":
                self.audio_player.play_bet_audio(player_number)
            
            elif action == "Call":
                self.players[player_number]['action_time'] = action_time
                self.audio_player.play_call_audio(player_number)

            elif action == "Check":
                self.players[player_number]['action_time'] = action_time
                self.add_log_entry({'method': 'update_player_action','player_number': player_number, 'role': player_role, 'action': action, 'time': action_time})
                self.audio_player.play_check_audio(player_number)
            
            elif action == "Fold":
                self.players[player_number]['action_time'] = action_time
                self.add_log_entry({'method': 'update_player_action','player_number': player_number, 'role': player_role, 'action': action, 'time': action_time})
                self.audio_player.play_fold_audio(player_number)
            
            elif action == "Raise":
                self.audio_player.play_raise_audio(player_number)


            # 1 player_number       ( 1 - 6 )
            # 2 player_role         (dealer, small blind, big blind)
            # 3 action              (fold, raise, call etc.)
            # 4 amount              (number)
            # 5 board_stage         (pre-flop, flop, river etc.)




        # Check if amount is a numeric value and update pot size
        if amount is not None:
            
            # Round the amount value to 2 decimal places. (4.43)
            rounded_amount = round(amount,2)

            self.players[player_number]['amount'] = rounded_amount
            
            current_pot_size = self.players[player_number].get('pot_size', 0.0)

            new_pot_size = current_pot_size + rounded_amount


             # Calculate new pot size and round it to 2 decimal places
            new_pot_size = round(new_pot_size, 2)
            
            # Update the pot size in the player's data
            self.players[player_number]['pot_size'] = new_pot_size

            player_action = self.players[player_number].get('action')

            #print(f"PLAYER {player_number} | ACTION = {player_action} | ADD AMOUNT = {rounded_amount} | CURRENT POT = {current_pot_size} |  NEW POT = {new_pot_size}")

            start_time = self.players.get(player_number, {}).get('turn_start_time')
            action_time = 0  

            if player_action in ("Raise", "Bet", "Call"):

                if(start_time is not None):
                    action_time = time.time() - self.players.get(player_number, {}).get('turn_start_time')
                    action_time = round(action_time, 0)  # Round to one decimal place

                    if action_time == 0:
                        action_time = 1

                    self.players[player_number]['action_time'] = action_time
                    
                self.add_log_entry({'method': 'update_player_action_raise','player_number': player_number, 'role': player_role, 'action': player_action, 'amount': rounded_amount, 'time': action_time, 'pot_size': new_pot_size})
           

            self.update_player_betting_history( player_number, role, action, amount, self.current_board_stage )
           
        if player_type is not None:
            self.players[player_number]['player_type'] = player_type #categorizes player by play style/type

        if exploitation_strategy is not None:
            self.players[player_number]['exploitation_strategy'] = exploitation_strategy #Strategic tips on how to exploit this player

        # Update player's stack size
        if stack_size is not None:
             # Round stack_size to 2 decimal places
            rounded_stack_size = round(stack_size, 2)
            self.players[player_number]['stack_size'] = rounded_stack_size
            #self.add_log_entry({'method': 'update_player_stack', 'player_number': player_number, 'stack_size': rounded_stack_size})

        # Update player won amount
        if won_amount is not None:
            won_amount_rounded = round(won_amount,2)
            self.players[player_number]['won_amount'] = won_amount_rounded
            self.players[player_number]['pots_won'] += 1

            won_counter = self.players.get(player_number, {}).get('pots_won')
            self.audio_player.play_wins_the_pot_audio(player_number)

            self.add_log_entry({'method': 'update_player_won','player_number': player_number, 'role': player_role, 'won_amount': won_amount_rounded, 'pots_won': won_counter })


    # *DONE*
    def get_current_player_turn(self):
        """
        Retrieve the player number of the player whose turn is currently set to True.
        """
        for player_number, player_info in self.players.items():
            if player_info['turn']:
                return player_number
        return 0  # Return None or handle the case where no player has the turn


    # *DONE*
    def update_community_cards(self, cards):
        """
        Update the community cards on the table.
        """
        self.community_cards = cards

        self.update_board_stage(cards)


    # *DONE*
    def update_board_stage(self, cards):

         # Count the number of community cards and set the stage
        num_cards = len(cards)

        if num_cards == 0:
            self.current_board_stage = "Pre-Flop"
            self.audio_player.play_board_pre_flop_audio()
        elif num_cards == 3:
            self.current_board_stage = "Flop"
            self.audio_player.play_board_flop_audio()
        elif num_cards == 4:
            self.current_board_stage = "Turn"
            self.audio_player.play_board_turn_audio()
        elif num_cards == 5:
            self.current_board_stage = "River"
            self.audio_player.play_board_river_audio()
        else:
            self.current_board_stage = "Unknown"  # Optional, for handling unexpected cases


        if self.current_board_stage != "Unknown":

            if num_cards > 0:
                self.add_log_entry({
                    'method': 'update_community_cards',
                    'Stage': self.current_board_stage,
                    'Table Cards': self.community_cards
                })



    def update_total_pot(self, pot):
        """
        Update the total amount of chips in the pot. // DONE
        """

        self.total_pot = pot    
        self.add_log_entry({'method': 'update_total_pot','Table Pot': pot})




    def update_dealer_position(self, position):
        """
        Update the position of the dealer button and adjust the roles for all players accordingly.
        """
        if not self.active_players:
            print("No active players available to update dealer position.")
            return

        # Ensure the active players list is sorted
        sorted_active_players = sorted(self.active_players)

        if position not in sorted_active_players:
            print(f"Dealer position {position} not found among active players.")
            return

        total_players = len(sorted_active_players)
        dealer_index = sorted_active_players.index(position)

        # Determine the index for each role
        sb_index    = (dealer_index + 1)    % total_players
        bb_index    = (dealer_index + 2)    % total_players
        utg_index   = (dealer_index + 3)    % total_players if total_players > 3 else None
        hj_index    = (dealer_index + 4)    % total_players if total_players > 4 else None
        mp_index    = (dealer_index + 5)    % total_players if total_players > 5 else None
        co_index    = (dealer_index + 6)    % total_players if total_players > 6 else None

        # Update roles for each player
        self.update_player(sorted_active_players[dealer_index], role='BTN') # Button
        self.update_player(sorted_active_players[sb_index], role='SB') # Small Blind
        self.update_player(sorted_active_players[bb_index], role='BB') # Big Blind

        if utg_index is not None:
            self.update_player(sorted_active_players[utg_index], role='UTG') # Under the Gun
        if hj_index is not None:
            self.update_player(sorted_active_players[hj_index], role='HJ') # Hijack
        if mp_index is not None:
            self.update_player(sorted_active_players[mp_index], role='MP') # Middle Position
        if co_index is not None:
            self.update_player(sorted_active_players[co_index], role='CO') # Cutoff

        dealer_player_number = sorted_active_players[dealer_index]
        small_blind_player_number = sorted_active_players[sb_index]
        big_blind_player_number = sorted_active_players[bb_index]

        # Play Audio for Hero player
        if dealer_player_number == self.hero_player_number:  
            self.audio_player.play_hero_is_the_dealer_audio()

        if small_blind_player_number == self.hero_player_number:  
            self.audio_player.play_hero_is_small_blind_audio()

        if big_blind_player_number == self.hero_player_number:  
            self.audio_player.play_hero_is_big_blind_audio()



    # Result of AI(GPT4-turbo) analysis -> Bet, Raise, Call, Fold | Action Types: Bluff, Value Bet, None
    def hero_action_type(self, action_type):

        if action_type == "Bluff":
            self.bluff_count += 1
        elif action_type == "Value Bet":
            self.value_bet_count += 1

        #print(f"Hero Action: {action} | Type: {[action_type]}")


    
    def calculate_heros_bluff_to_value_ratio(self):
        """
        Calculate the bluff-to-value ratio.

        : bluff_count: Number of times the player has bluffed.
        : value_bet_count: Number of times the player has made a value bet.
        : Return: Calculated bluff-to-value ratio.
        """
        # Handling the case when value bet count is zero to avoid division by zero
        if self.value_bet_count == 0:
            if self.bluff_count == 0:
                # If both bluff count and value bet count are zero, ratio is undefined
                return None
            else:
                # If only value bet count is zero, ratio is infinitely large
                return None
        
        # Calculating the ratio
        ratio = self.bluff_count / self.value_bet_count

        # Display the result
        #print(f"Hero: Bluff-to-Value Ratio: {ratio}")

        return ratio


    # TODO - IMPLEMENT THIS FOR ALL PLAYERS
    def update_hands(self, played):
        """
        Update the player's hand statistics.

        :param played: Boolean indicating if the player played the hand.
        """
        self.total_hands_dealt += 1
        if played:
            self.hands_played += 1

    # TODO - IMPLEMENT THIS FOR ALL PLAYERS
    def get_play_percentage(self):
        """
        Calculate the percentage of hands the player has played.

        :return: The percentage of hands played.
        """
        if self.total_hands_dealt == 0:
            return 0
        return (self.hands_played / self.total_hands_dealt) * 100



    def update_player_betting_history(self, player_number, player_role, action, amount, board_stage):
        """
        Add a record to the betting history to a specific player.
        
        Parameters:
        - player_number: The number identifying the player.
        - action: The action taken by the player (bet, call, raise, check, fold).
        - amount: The size of the bet or raise made by the player.
        - board_stage: The current stage of the game (pre-flop, flop, turn, river).
        - player_role: The position of the player (dealer-D, small blind-SB, big blind-BB).
        """
        betting_history_entry = {
            'player_number': player_number,
            'player_role': player_role,
            'action': action,
            'amount': amount,
            'game_stage': board_stage
        }

        self.betting_history.append(betting_history_entry)
    

    def reset_for_new_round(self):
        """
        Reset the game state for a new round.
        This method is only executed if more than 2 seconds have passed since the last execution.
        """
        current_time = time.time()

        if current_time - self.last_round_end_time > 5:  # Check if more than X seconds have passed

            self.round_count += 1 #Add to the count of rounds played 

            save_round_info = self.get_log()
                
            # Save round information to file
            self.save_data_to_file(save_round_info)

            # Clear the log before starting new round
            self.log.clear()
            
            self.trim_logs()

            self.community_cards = []  # Reset the List of community cards

            self.hero_cards = [] # Reset Hero(Player1) cards

            self.dealer_position = -1 # Reset Player number who is the current dealer. Default -1(none) 

            self.current_board_stage = 'Pre-Flop'  # Current stage of the game 

            self.total_pot = 0  # Reset the total amount of pot on table 
            
            bluff_to_value_ratio = self.calculate_heros_bluff_to_value_ratio()

            self.add_log_entry({'method': 'line','Limier': '---------------------'})

            self.add_log_entry({'method': 'reset_for_new_round','Round': self.round_count})

            self.add_log_entry({'method': 'update_total_players'})


            self.add_log_entry({'method': 'update_blinds', 'small_blind': self.small_blind, 'big_blind': self.big_blind})

            if bluff_to_value_ratio is not None: self.add_log_entry({'method': 'hero_bluff_to_value_ratio', 'bluff_value_ratio': bluff_to_value_ratio})

            # Reset the relevant values for each player and log their stack size
            for player_number, player in self.players.items():
                player['cards'] = None
                player['turn'] = None
                player['turn_start_time'] = None
                player['action'] = "None"
                player['action_time'] = 0.0
                player['amount'] = 0.0
                player['pot_size'] = 0.0

                # Log each player's stack size
                self.add_log_entry({'method': 'update_players_stacks','player_number': player_number,'stack_size': player.get('stack_size', 0.0), 'role': player.get('role')})

            if self.hero_player_number is not None and self.hero_player_number > 0:

                self.hero_cards = self.players.get(self.hero_player_number, {}).get('cards')

                self.add_log_entry({'method': 'update_player_hero','player_number': self.hero_player_number, 'hero': True })

                if self.hero_cards:
                    self.add_log_entry({'method': 'update_player_cards','player_number': self.hero_player_number, 'cards': self.hero_cards })


            self.add_log_entry({'method': 'line','Limier': '---------------------'})

            self.add_log_entry({'method': 'update_community_cards','Stage': 'Pre-Flop','Table Cards': ''})
            
            self.last_round_end_time = current_time

        
    def trim_logs(self, max_entries=500):
        # Trim the list to the last 'max_entries' elements
        self.all_round_logs = self.all_round_logs[-max_entries:]


    def save_data_to_file(self, data, file_name='round_data.txt', directory='Saved_Info'):
        """
        Save the provided data to a file.

        :param data: Data to be saved.
        :param file_name: Name of the file where data will be saved.
        :param directory: Directory where the file will be located.
        """
        # Create the directory if it does not exist
        os.makedirs(directory, exist_ok=True)

        # Full path for the file
        full_path = os.path.join(directory, file_name)

        # Open the file with utf-8 encoding and append the data
        with open(full_path, 'a', encoding='utf-8') as file:
            for entry in data:
                file.write(entry + '\n')
            file.write("\n\n")  # Two line breaks after the data
