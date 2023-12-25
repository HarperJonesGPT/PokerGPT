import time
from colorama import Fore 
import pygame 
import json

class PokerAssistant:


    def __init__( self, openai_client, hero_info, game_statem, hero_action, audio_player ):

        print("Initializing PokerAssistant...")

        pygame.init()  # Initialize the pygame module for audio playback


        self.client             = openai_client 

        self.hero_info          = hero_info

        self.game_state         = game_statem

        self.audio_player       = audio_player             

        self.hero_action        = hero_action     
    
    # ------------------------------------------------------------------------------------------------

    def AnalyzeAI( self, hero_buttons_map, poker_game_data ):

        print(F"{Fore.YELLOW}AnalyzeAI(): Starting AI analysis...")

        gpt4_output = self.analyze_game_state_with_gpt4( hero_buttons_map, poker_game_data )
        
        print(F"{Fore.YELLOW}AnalyzeAI():Finished AI analysis...")

        if gpt4_output is not None:

            print(F"{Fore.GREEN}----------------------------------------------")
            print(F"{Fore.GREEN}GPT4 OUTPUT:")
            print(F"{Fore.GREEN}----------------------------------------------")
            print(F"{Fore.GREEN} {gpt4_output}")
            print(F"{Fore.GREEN}----------------------------------------------")

            return self.extract_hero_action_details_from_gpt4_output( hero_buttons_map, gpt4_output )
    
        else:
            print(F"{Fore.RED}Failed to get response in 26 seconds, so I will FOLD the hand now..")
            self.execute_check_or_fold(hero_buttons_map)

        return None
    

    # ------------------------------------------------------------------------------------------------
    
    #User message for injecting the poker data into the gpt-4 analysis prompt
    def create_user_prompt( self, realtime_game_data):

        print(F"{Fore.YELLOW}AnalyzeAI(): Creating user prompt...")

        hero_round_actions_history  = self.hero_info.get_recent_actions()

        hero_strategy_history       = self.hero_info.get_recent_strategies()

        hero_tactics_history        = self.hero_info.get_recent_tactics()

        active_player_analysis = ""
        #-----------------------------------------
        # Loop through all 6 players
        for player_number in range(1, 7):  # range(1, 7) generates numbers from 1 to 6

            player_info = self.game_state.players[player_number]
            player_last_action = player_info.get('action')

            if 'Fold' not in player_last_action:

                player_type         = player_info.get('player_type')
                player_strategy     = player_info.get('exploitation_strategy')
                  
                if player_strategy and 'None' not in player_strategy:
                        player_data = f"#Player {player_number} Analysis:\nType: {player_type}\nExploitation Strategy:\n{player_strategy}\n"
                        active_player_analysis += player_data + "\n----------------------\n"


        user_prompt = f"""
                        #Hero Actions History:
                        '''
                        {hero_round_actions_history}
                        '''
                        #Hero Strategy History:
                        '''
                        {hero_strategy_history}
                        '''
                        #Hero Tactics History:
                        '''
                        {hero_tactics_history}
                        '''
                        ---------------------------

                        #Player Analysis: 
                        '''
                        {active_player_analysis}
                        '''
                        ---------------------------

                        #Texas Holdem(6 Players, No-Limit, Cash game) Poker data:
                        '''
                        {realtime_game_data}
                        Heros Players Turn:
                        '''
                        """

        return user_prompt
    

    # ------------------------------------------------------------------------------------------------

    def analyze_game_state_with_gpt4(self, hero_buttons_active, realtime_game_data):
        try:

           # Format the hero_buttons_active values to include only actions
            available_actions = '\n'.join([f"- {info['action']}" for info in hero_buttons_active.values()])

            print(f"{Fore.GREEN} available_actions: \n' {available_actions}")

            # Create the user prompt with the real-time game data and available actions
            user_message_prompt = self.create_user_prompt( realtime_game_data )


            #print(F"{Fore.BLUE}analyze_game_state_with_gpt4() -> USER INPUT PROMPT:\n {user_message_prompt}")
            
            start_time = time.time()  # Record the start time before making the API call

            # Check if available_actions contains any actions
            actions_prompt = "#Available Actions:\n" + available_actions if available_actions else ""

            response = self.client.chat.completions.create(
                model=  "gpt-4-1106-preview",
                #model=  "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"""
                        You are Hero player. 
                        Your objective is to analyze real-time online poker data from a 6-max Online Texas Holdem (No Limit, Cash game) and suggest the next action for the hero.

                        {actions_prompt}
                     
                        --------------------------

                        #HARD RULES(follow STRICTLY!):

                        - ACTIONS: strictly make decisions based on #Available Actions.

                        - STRATEGY: 
                        1. Focus on dynamic and unpredictable Exploitative poker strategies, mixed with occational (Game Theory Optimied) GTO plays.

                        - ALL-IN: 
                        1. Allowed Pre-flop with premium hands if we are likely to steal blinds.
                        2. When Hero have been Folding a lot Pre-Flop recently and the opponents are likely to fold. 

                        - RAISING: DO NOT raise on the Turn/River when Heros cards don't connect to the board, especially against tight players.

                        - UNPREDICTABILITY: 
                        1. Always keep opponents guessing by mixing actions between calling, checking, betting and raising, based on the history of Hero actions(if available). 
                        2. If you recently folded, bet or check instead. If you recently raised, check instead. Occationally bet/raise with weak cards to confuse opponents.
                        3. Mix up strategy based on history of strategies to confuse, deceive and exploit opponents.
                        4. Mix up tactics based on history of tactics to confuse, deceive and exploit opponents.
                        5. Vary bet sizing based on history of bet/raising values to confuse, deceive and exploit opponents.

                        --------------------------

                        #GENERAL GUIDELINES(follow depending on the context)
                        
                        - RANGE CONSIDERATION: Be aware of possible ranges of opponents when deciding to bet or raise.

                        - POSITIONAL AWARENESS: Be more aggressive in late positions with strong hands, especially in short-handed situations. Ensure your aggression is calculated and not just based on position.

                        - CHECKING: Occationally Check/Call with strong hands to let other players build the pot and disquise our strong hand.

                        - POT CONTROL: Focus on controlling the pot size to manage risk, especially with marginal hands in late positions(turn, river).

                        - FOLDING: Fold when the odds are against you, especially in response to strong bets from conservative/tight players(that play mostly strong/premium hands).

                        - RAISE AMOUNTS: Adjust your pre-flop raise amounts based on the stakes, action history, number of limpers, your position and any other relevant data. 

                        - BET SIZING: Focus on optimizing bet sizes to maximize value from weaker hands and protect against draws. 

                        - BANKROLL MANAGEMENT: Monitor and manage your stack size, adapting your bet sizing and risk-taking accordingly.

                        - BLUFFING VS VALUE BETTING> Strategically balance bluffing with value betting while considering opponents actions, ranges and tendencies.

                        Note: You tend to over value hands and over bet post-flop, so minimize bet sizing.

                        #Use the following 'strategy'-s:
                        - GTO
                        - Exploit
                        - Mixed
                     
                        #Use the following 'tactic'-s: 
                        - Semi-Bluff
                        - Bluff
                        - Probe Bet
                        - Value Bet
                        - Check-Raise
                        - Trap Play
                        - Floating
                        - Steal Attempt
                        - Exploit
                        - Weak Hand
                        - None

                        OUTPUT JSON FORMAT:
                        {
                            {
                                "strategy": "string",
                                "tactic": "string",
                                "explanation": "Provide short and concise instructions of the strategy and tactics for the next hands.",
                                "action": "string",
                                "amount": "number"
                            }
                        }
                    """},
                    {"role": "user", "content": user_message_prompt}
                ], 
               
                temperature         = 0.2,
                max_tokens          = 300,
                top_p               = 0.95,
                frequency_penalty   = 0,
                presence_penalty    = 0,
                response_format     = {"type": "json_object"}
            )


            end_time = time.time()  # Record the end time after receiving the response

            print("")
            print("-------------------------------------------------------------------")
            print(f"analyze_game_state_with_gpt4() -> Time taken: {end_time - start_time} seconds")  # Calculate and print the time taken
            # Extract the GPT-4 response
            gpt_response = response.choices[0].message.content

            return gpt_response
        

        except self.client.error.OpenAIError as e:

            print(F"{Fore.RED}An error occurred with the OpenAI API: {e}")

        except Exception as e:

            print(F"{Fore.RED}An error occurred: {e}")

        return None
    

    # ------------------------------------------------------------------------------------------------

    # Read the response from GPT4 analysis and extract actions
    def extract_hero_action_details_from_gpt4_output(self, hero_buttons_map, gpt4_output):
        """
        Extract content from a given GPT-4 output text string based on the tag-based format.

        :param gpt4_output: String containing the poker action details from GPT-4 output.
        """ 
        
        extracted_details = {
            'Action':       None,
            'Amount':       None,
            'Tactic':       None,
            'Strategy':     None,
            'Explanation':  None
        }

        try:
            # Parse the JSON data
            data = json.loads(gpt4_output)
            
            # Search for matches in the text
            explanation_match       = data.get('explanation')
            strategy_match          = data.get('strategy')
            action_match            = data.get('action')
            action_amount_match     = float(data.get('amount'))
            action_type_match       = data.get('tactic')


            extracted_details['Amount'] = action_amount_match

            if action_match:
                extracted_action = action_match
                extracted_details['Action'] = extracted_action

                # Find the corresponding button coordinates in hero_buttons_active
                button_coordinates = (0.516, 0.907)

                print(F"{Fore.CYAN}extracted_action = {extracted_action}")

                for button_info in hero_buttons_map.values():
                    
                    #print(F"{Fore.CYAN}button_info = {button_info}")

                    # Check if the first four letters of the action match
                    if button_info['action'][:4].lower() in extracted_action.lower():
                        button_coordinates = button_info['pos']
                        matching_action = button_info['action']
                        #print(F"{Fore.CYAN}execute_action = {matching_action}")
                        break

                if button_coordinates and len(button_coordinates) == 2:
                   
                    self.hero_action.execute_action(button_coordinates, extracted_action, action_amount_match)

                    self.audio_player.play_speech(f"Hero ACTION: {extracted_action} {action_amount_match} dollars. Go!")
                else:
                    self.hero_action.execute_action(None, "Fold", None)
                    print(f"{Fore.RED}No matching button found for action '{extracted_action}'.")

                
                extracted_details['Tactic']     = action_type_match
                #self.audio_player.play_speech(action_type_match)

                extracted_details['Strategy']       = strategy_match
                #self.audio_player.play_speech(strategy_match)

                extracted_details['Explanation']    = explanation_match
                #self.audio_player.play_speech(explanation_match)

        except Exception as e:
            print(F"{Fore.RED}An error occurred during extraction: {e}")
            #self.execute_check_or_fold(hero_buttons_map)

        return extracted_details
    

    def execute_check_or_fold(self, hero_buttons_active):

        fold_coordinates    = None
        check_coordinates   = None

        # Iterate through available actions to find "Fold" or "Check"
        for button_info in hero_buttons_active.values():

            if button_info['action'] == "Fold":
                fold_coordinates = button_info['pos']
            elif button_info['action'] == "Check":
                check_coordinates = button_info['pos']

        # Prioritize "Fold" if available, else use "Check"
        if fold_coordinates:
            self.hero_action.execute_action(fold_coordinates, "Fold", 0)
        elif check_coordinates:
            self.hero_action.execute_action(check_coordinates, "Check", 0)
        else:
            print(f"{Fore.RED} execute_check_or_fold(): Neither 'Check' nor 'Fold' action available.")
      

    def format_historical_data(self, historical_data):
        print(F"{Fore.RED}historical_data = \n {historical_data}")
        print(F"{Fore.RED}--------------------------------------")

        formatted_output = ""
        for item in historical_data:
            formatted_item = item.replace("'", "")  # Remove single quotes
            for part in formatted_item.split(', '):
                formatted_output += part + "\n"

        return formatted_output


    # This method is called by read_poker_table.py
    def analyze_players_gpt4(self, historical_data):
        try:
            formatted_data = self.format_historical_data(historical_data)

            if len(formatted_data) == 0:
                print(F"{Fore.RED}Error: analyze_players_gpt4() historical_data is NULL. Returning...")
                return
            
            print("")
            print(f"{Fore.LIGHTYELLOW_EX} FORMATTED HISTORIAL DATA:")
            print(f"{Fore.LIGHTYELLOW_EX} {formatted_data}")
            print("")

            start_time = time.time()  # Record the start time before making the API call

            print("analyze_players_gpt4() -> Analyzing players with GPT-4 Turbo...")

            response = self.client.chat.completions.create(
                model=  "gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": """
                    Your task is to analyze historical game data from a 6-player Texas Holdem Online poker game (No-limit, Cash) to develop strategies for the Hero player to exploit opponents weaknesses. 
                     
                    The analysis should be nuanced and comprehensive, taking into account a wide array of behavioral data and patterns( action patterns, action timings, bet sizing, positions, ranges, psychology etc). 
                    Always use LOGIC and REASONING. 
                    
                    #Use the following categories for 'player_style' classification:
                    
                    - Tight-Passive (The Rock)
                    - Loose-Passive (The Calling Station)
                    - Tight-Aggressive (TAG)
                    - Loose-Aggressive (LAG)
                    - Maniac
                    - Nit
                    - Hybrid Player
                    - Shark
                    - The Fish
                    - The Grinder
                    - The Trapper
                    - The Gambler
                    
                    --------------------------------------------------
                    
                    #Limitations:
                    - Do NOT output data for the Hero.
                     
                    OUTPUT JSON FORMAT:
                    {
                        "players": [
                            {
                                "player_number: "number",
                                "player_id": "string",
                                "player_style": "string",
                                "exploitation_strategy": "Actionable, clear and concise instructions for the Hero to exploit this opponent."
                            },
                        ]
                    }
                    """},
                    {"role": "user", "content": formatted_data}
                ],
                temperature         = 0.1,
                max_tokens          = 4000,
                top_p               = 0.95,
                frequency_penalty   = 0,
                presence_penalty    = 0,
                response_format     = {"type": "json_object"}
            )

            end_time = time.time()  # Record the end time after receiving the response

            print("-------------------------------------------------------------------")
            print(f"analyze_players_gpt4() -> Time taken: {end_time - start_time} seconds")  # Calculate and print the time taken
            print("-------------------------------------------------------------------")
            # Extract the GPT-4 response
            gpt_response = response.choices[0].message.content

            print("")
            print(f"{Fore.LIGHTYELLOW_EX}-------------------------------------------------------------------")
            print(f"{Fore.LIGHTYELLOW_EX}RAW GTP4 RESPONSE:")
            print(f"{Fore.LIGHTYELLOW_EX}{gpt_response}")
            print(f"{Fore.LIGHTYELLOW_EX}-------------------------------------------------------------------")
            print("")

            if gpt_response:
                self.parse_and_update_player_analysis(gpt_response)
        
        except Exception as e:
            print(f"An error occurred during GPT-4 analysis: {e}")
        

    def parse_and_update_player_analysis(self, player_analysis_json):

        #print(f"{Fore.YELLOW}Parsing player analysis JSON.")

        data = json.loads(player_analysis_json)
        player_data_to_write = []  # List to store data for writing to file

        for player in data['players']:

            player_number = int(player['player_number'])  # Convert to integer
            #print(f"{Fore.YELLOW}Processing player {player_number}.")

            player_type_str             = "- " + player['player_style']

            exploitation_strategy_str   = "- " + player['exploitation_strategy']
            
            # Append formatted data to the list
            player_data_to_write.append(f"Player{player_number}:\n{player_type_str}\n{exploitation_strategy_str}\n")

            if 1 <= player_number <= 6:
                self.game_state.update_player(player_number, player_type=player_type_str, exploitation_strategy=exploitation_strategy_str)
            else:
                print(f"{Fore.YELLOW}Invalid player number: {player_number}. Skipped updating.")

        # Read historical data from the file
        with open('Saved_info/player_analysis.txt', 'w') as file:
            file.writelines(player_data_to_write)

        print(f"{Fore.YELLOW}Completed parsing and updating player analysis.")