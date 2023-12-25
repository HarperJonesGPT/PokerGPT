import random
import tkinter      as tk
import tkinter.font as tkFont
from tkinter        import scrolledtext
from tkinter        import ttk

class GUI:

    def __init__( self, game_state, poker_assistant):

        self.game_state         = game_state

        self.poker_assistant    = poker_assistant

        self.root = tk.Tk()

        # Set the background color of the root window
        self.root.configure(background='#171821')


        # List of possible titles
        possible_titles = ["dfsdfdsfsd", "24234234", "552423", "24324", "123424", "8967991", "507341", "412355", "5234234655", "664544545211", "343242343256, 2443243252532, 55525, 65465345"]

        # Select a random title from the list
        random_title = random.choice(possible_titles)

        self.root.title(random_title)  # Set the random title
        

         # Get screen width and height
        screen_width    = self.root.winfo_screenwidth()
        screen_height   = self.root.winfo_screenheight()

         # Set window size to match screen size
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Add widgets
        self.add_widgets()

        # Start the polling loop
        self.polling_update()



    def add_widgets(self):
        padding = {'padx': 10, 'pady': 10}
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=14, weight='bold')
        tableFont = tkFont.Font(family="Lucida Grande", size=14)  # Font for Treeview elements

        input_width = 10  # Adjust width of input fields as needed
        
        # Configure the Treeview font
        style = ttk.Style(self.root)
        style.configure("Custom.Treeview", font=tableFont, padding=15)
        style.configure("Custom.Treeview.Heading", font=self.fontStyle)  # Heading font

        # Create a Treeview widget for player information
        self.player_tree = ttk.Treeview(self.root, height=7, style="Custom.Treeview")
        self.player_tree['columns'] = ('Player', 'Status', 'Role', 'Cards', 'Turn', 'Action', 'Amount', 'Pot Size', 'Stack Size', 'Won Amount','Total Wins', 'Play Style')

        # Hide the default tree column
        self.player_tree.column('#0', width=0, stretch=tk.NO)
        self.player_tree.heading('#0', text='')

        # Define the column headings
        for col in self.player_tree['columns']:
            self.player_tree.heading(col, text=col)
            self.player_tree.column(col, width=140, anchor='center')  # You can adjust the width as necessary

        # Position the Treeview widget
        self.player_tree.grid(row=1, column=0, columnspan=12, pady=10, padx=10, sticky='nsew')


        # Configure the first two columns to not expand unnecessarily
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)



        # Total Players and its Entry field
        self.total_players_label = tk.Label(self.root, text="Total Players", font=self.fontStyle, bg='#171821', fg='white')
        self.total_players_label.grid(row=0, column=0, sticky="w", **padding)
        self.total_players_info = tk.Text(self.root, height=1, width=input_width, bg='#171821', fg='white', font=self.fontStyle)
        self.total_players_info.grid(row=0, column=1, sticky="w", **padding)


        # Hero Player1 Cards and its Entry field
        self.hero_cards_label = tk.Label(self.root, text="Hero Cards", font=self.fontStyle, bg='#171821', fg='white')
        self.hero_cards_label.grid(row=2, column=0, sticky="w", **padding)
        self.hero_cards_info = tk.Text(self.root, height=1, width=input_width*2, bg='#171821', fg='white', font=self.fontStyle)
        self.hero_cards_info.grid(row=2, column=1, sticky="w", **padding)


        # Community Cards and its Entry field
        self.community_cards_label = tk.Label(self.root, text="Community Cards", font=self.fontStyle, bg='#171821', fg='white')
        self.community_cards_label.grid(row=3, column=0, sticky="w", **padding)
        self.community_cards_info = tk.Text(self.root, height=1, width=input_width*2, bg='#171821', fg='white', font=self.fontStyle)
        self.community_cards_info.grid(row=3, column=1, sticky="w", **padding)


        # Board Stage and its Entry field
        self.board_stage_label = tk.Label(self.root, text="Board Stage", font=self.fontStyle, bg='#171821', fg='white')
        self.board_stage_label.grid(row=4, column=0, sticky="w", **padding)
        self.board_stage_info = tk.Text(self.root, height=1, width=input_width, bg='#171821', fg='white', font=self.fontStyle)
        self.board_stage_info.grid(row=4, column=1, sticky="w", **padding)


        # Total Pot Size and its Entry field
        self.pot_size_label = tk.Label(self.root, text="Total Pot Size", font=self.fontStyle, bg='#171821', fg='white')
        self.pot_size_label.grid(row=5, column=0, sticky="w", **padding)
        self.pot_size_info = tk.Text(self.root, height=1, width=input_width, bg='#171821', fg='white', font=self.fontStyle)
        self.pot_size_info.grid(row=5, column=1, sticky="w", **padding)


        # Dealer Position and its Entry field
        self.dealer_position_label = tk.Label(self.root, text="Dealer Position", font=self.fontStyle, bg='#171821', fg='white')
        self.dealer_position_label.grid(row=6, column=0, sticky="w", **padding)
        self.dealer_position_info = tk.Text(self.root, height=1, width=input_width, bg='#171821', fg='white', font=self.fontStyle)
        self.dealer_position_info.grid(row=6, column=1, sticky="w", **padding)


        # Round Count and its Entry field
        self.round_count_label = tk.Label(self.root, text="Rounds", font=self.fontStyle, bg='#171821', fg='white')
        self.round_count_label.grid(row=7, column=0, sticky="w", **padding)
        self.round_count_info = tk.Text(self.root, height=1, width=input_width, bg='#171821', fg='white', font=self.fontStyle)
        self.round_count_info.grid(row=7, column=1, sticky="w", **padding)


        # Log Entries and its ScrolledText field
        self.log_info = scrolledtext.ScrolledText(self.root, height=8, width=80, bg='#171821', fg='white', font=self.fontStyle)
        self.log_info.grid(row=8, column=0, columnspan=5, pady=10, padx=10, sticky="nw")


         # Log Entries and its ScrolledText field
        self.ai_log_info = scrolledtext.ScrolledText(self.root, height=10, width=80, bg='#171821', fg='white', font=self.fontStyle)
        self.ai_log_info.grid(row=9, column=0, columnspan=5, pady=10, padx=10, sticky="nw")



    def update_info(self):
        
        # Clear the existing content in the Treeview
        for i in self.player_tree.get_children():
            self.player_tree.delete(i)

        # Sort the player numbers
        sorted_player_numbers = sorted(self.game_state.players.keys(), key=int)

        # Populate the Treeview with new player information
        for player_number in sorted_player_numbers:
            player_info = self.game_state.players[player_number]

            # Handle 'cards' field when it is None or not a list
            cards = player_info.get('cards', [])
            cards_display = ', '.join(cards) if isinstance(cards, list) else 'No Cards'

            # Player', 'Status', 'Role', 'Hero', 'Cards 'Turn', 'Action', 'Amount', 'Pot Size', 'Stack Size', 'Won Amount','Total Wins', 'Play Style')
            self.player_tree.insert('', 'end', values=(
                player_info.get('name', 'N/A'),  # Replace 'N/A' with your default values or checks
                player_info.get('status', 'N/A'),
                player_info.get('role', 'N/A'),
                cards_display,
                'Yes' if player_info.get('turn', False) else 'No',  # Turn is a boolean
                player_info.get('action', ''),
                player_info.get('amount', ''),
                player_info.get('pot_size', ''),
                player_info.get('stack_size', ''),
                player_info.get('won_amount', ''),
                player_info.get('pots_won', ''),
                player_info.get('play_style', '')
                #player_info.get('psychology', '')
            ))

        # Update the number of active players on the table
        self.total_players_info.delete("1.0", tk.END)
        self.total_players_info.insert(tk.END, str(len(self.game_state.active_players)))

         # Update the Hero player cards
        community_cards = ", ".join(self.game_state.hero_cards) if self.game_state.hero_cards else "None"
        self.hero_cards_info.delete("1.0", tk.END)
        self.hero_cards_info.insert(tk.END, community_cards)

        # Update the community cards
        community_cards = ", ".join(self.game_state.community_cards) if self.game_state.community_cards else "None"
        self.community_cards_info.delete("1.0", tk.END)
        self.community_cards_info.insert(tk.END, community_cards)


        # Update the board stage with appropriate color
        board_stage = self.game_state.current_board_stage  
        self.board_stage_info.delete('1.0', tk.END)
        self.board_stage_info.insert('1.0', board_stage)


        # Configure tag styles for different board stages
        self.board_stage_info.tag_configure('pre_flop', foreground='#2968c7')
        self.board_stage_info.tag_configure('flop', foreground='#29c795')
        self.board_stage_info.tag_configure('turn', foreground='#c76f29')
        self.board_stage_info.tag_configure('river', foreground='#64c729')


        # Apply the tag based on the board stage
        if board_stage == 'Pre-Flop':
            self.board_stage_info.tag_add('pre_flop', '1.0', 'end')
        elif board_stage == 'Flop':
            self.board_stage_info.tag_add('flop', '1.0', 'end')
        elif board_stage == 'Turn':
            self.board_stage_info.tag_add('turn', '1.0', 'end')
        elif board_stage == 'River':
            self.board_stage_info.tag_add('river', '1.0', 'end')


        # Update the total pot size
        self.pot_size_info.delete("1.0", tk.END)
        self.pot_size_info.insert(tk.END, str(self.game_state.total_pot))

        # Update the dealer position
        self.dealer_position_info.delete("1.0", tk.END)
        self.dealer_position_info.insert(tk.END, str(self.game_state.dealer_position))

        # Update the round count
        self.round_count_info.delete("1.0", tk.END)
        self.round_count_info.insert(tk.END, str(self.game_state.round_count))


        # Update log entries
        log_entries = "\n".join(self.game_state.get_log())
        self.log_info.delete("1.0", tk.END)
        self.log_info.insert(tk.END, log_entries)
        self.log_info.see(tk.END)  # Scroll to the end of the log

        # Update AI actins log entries 
        last_added_element = self.game_state.last_hero_action_log
        self.ai_log_info.delete("1.0", tk.END)
        self.ai_log_info.insert(tk.END, last_added_element)
        self.ai_log_info.see(tk.END)  # Scroll to the end of the log



    def polling_update(self):
        # Update the GUI with the latest information
        self.update_info()
        # Schedule the next poll in 1000ms (1 second)
        self.root.after(100, self.polling_update)


    def run(self):
        self.root.mainloop()