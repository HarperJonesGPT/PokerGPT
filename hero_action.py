import time
from colorama import Fore
import pyautogui
import random

class HeroAction:
    
    def __init__( self, poker_window ):
        
        self.window = poker_window

        self.window_activation_error_reported = False

        # Mapping of actions to their corresponding button positions
        """action_to_button = {
            'Fold':     (0.516, 0.909),  # Button1 = 'Fold'
            'Check':    (0.679, 0.909),  # Button2 = 'Check' or 'Call'
            'Call':     (0.679, 0.909),  # Button2 = 'Check' or 'Call'
            'Raise':    (0.842, 0.909),  # Button3 = 'Raise' or 'Call' or 'Bet'
            'Bet':      (0.842, 0.909),  # Button3 = 'Raise' or 'Call' or 'Bet'
        }"""
    #-----------------------------------------------------
    
    # Call in GameState to execute the AI suggested action in Pokerstars window
    def execute_action( self, button_coordinates, action, amount):

        self.activate_window()

        if button_coordinates is None:
            
            first_button = (0.516, 0.907)
            self.click_button(first_button)

            second_button = (0.679, 0.907)
            self.click_button(second_button)
            return
        
        # Split the action string and take the first part
        action = action.split()[0]
    
        match action:
            case 'Bet':
                self.bet(button_coordinates, amount)
            case 'Raise':
                self.raise_bet(button_coordinates, amount)
            case 'All':
                self.all_in(button_coordinates)
            case 'Call' | 'Fold' | 'Check' | 'Resume' | 'Cash Out':
                self.click_button(button_coordinates)
            case _:
                print(f"{Fore.RED}HeroActions -> execute_action(): Player Action {action} not recognized.")



    #-----------------------------------------------------

    def bet( self, button_coordinates, amount ):

        self.click_and_drag_input_box(0.728, 0.858, 0.642, 0.858)
        
        if amount > 0:
            self.input_bet_raise_amount(amount)

        self.click_button(button_coordinates)



    def raise_bet( self, button_coordinates, amount ):

        self.click_and_drag_input_box(0.728, 0.858, 0.642, 0.858)

        if amount > 0:
            self.input_bet_raise_amount(amount)

        self.click_button(button_coordinates)
       
    

    def all_in( self, button_coordinates ):
        self.click_max_bet_button()
        self.click_button(button_coordinates)

    #-----------------------------------------------------
    
    def click_button( self, button_coordinates ):
        """Click a button in the poker client window."""

        if not self.window:
            print(F"{Fore.RED}HeroActions -> click_button(): Window not located. Please locate the window first.")
            return

        # Get the button coordinates
        button_x, button_y = button_coordinates

        # Add randomness to the position
        random_position_x = random.uniform(0.0, 0.05)
        random_position_y = random.uniform(0.0, 0.05)

        # Calculate the absolute position of the button
        abs_x = self.window.left    + int(self.window.width     * (button_x + random_position_x))
        abs_y = self.window.top     + int(self.window.height    * (button_y + random_position_y))

        random_duration = random.uniform(0.1, 0.2)

        # Move the mouse cursor to the position for visual confirmation
        pyautogui.moveTo(abs_x, abs_y, duration=0.1)

        # Perform the click
        pyautogui.click(abs_x, abs_y)

        print(F"{Fore.YELLOW}Button clicked at x={abs_x}, y={abs_y}")

         # Move the mouse cursor to the position for visual confirmation
        pyautogui.moveTo((self.window.width/2)+random.uniform(0, 500), (self.window.height/2)+random.uniform(0, 500), duration=random_duration)


    #-----------------------------------------------------

    # Sets the maximum bet size (so we can go All-in!) *NOT USED*
    def click_max_bet_button(self):
        """Click the 'Max' button in the poker client window."""

        if not self.window:
            print(F"{Fore.RED}HeroActions -> Window not located. Please locate the window first.")
            return

        random_position_add = random.uniform(-0.02, 0.02)

        # Calculate the absolute position of the 'Bet' button
        abs_x = self.window.left    + int(self.window.width     * (0.945 + random_position_add))
        abs_y = self.window.top     + int(self.window.height    * (0.809 + random_position_add))


        random_cursor_speed = random.uniform(0.01, 0.1)

         # Move the mouse cursor to the position for visual confirmation
        pyautogui.moveTo(abs_x, abs_y, duration=random_cursor_speed)  # Move the cursor over 1 second


        # Perform the click
        pyautogui.click(abs_x, abs_y)

        print(F"{Fore.YELLOW}HeroActions -> Max bet Button clicked at x={abs_x}, y={abs_y}")

    
    def input_bet_raise_amount(self, amount):
        """Simulate keyboard input for betting or raising a specific amount."""

        amount_str = str(amount)  # Convert the amount to a string

        # Generate a random float value
        random_sleep_time   = random.uniform(0.1,   0.2)
        write_speed         = random.uniform(0.01,  0.1)

        time.sleep(random_sleep_time)  

        pyautogui.write(amount_str, interval=write_speed)  # Type out the amount

        print(F"{Fore.YELLOW}HeroActions -> Input bet/raise amount: {amount_str}")

    #-----------------------------------------------------

    def click_and_drag_input_box(self, start_rel_x, start_rel_y, end_rel_x, end_rel_y, duration=0.1):
        """
        Mouse start coordinates in relative space:
        0.728, 0.858

        Mouse end coordinates in relative space:
        0.649, 0.858

        Simulates a click and drag action using relative coordinates within the window.

        :param start_rel_x: Relative X coordinate of the starting point.
        :param start_rel_y: Relative Y coordinate of the starting point.
        :param end_rel_x: Relative X coordinate of the end point.
        :param end_rel_y: Relative Y coordinate of the end point.
        :param duration: Time taken for the drag action in seconds.
        """
        if not self.window:
            print("HeroActions -> Window not located. Please locate the window first.")
            return

        # Calculate absolute coordinates from relative coordinates
        start_abs_x     = self.window.left  + int(self.window.width     * start_rel_x)
        start_abs_y     = self.window.top   + int(self.window.height    * start_rel_y)
        end_abs_x       = self.window.left  + int(self.window.width     * end_rel_x)
        end_abs_y       = self.window.top   + int(self.window.height    * end_rel_y)

        # Perform the click and drag
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=duration)
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.1, 0.2))  # Short delay to ensure the mouse down event is registered
        pyautogui.moveTo(end_abs_x, end_abs_y, duration=duration)
        pyautogui.mouseUp()


      #-----------------------------------------------------

    def activate_window(self):
        """Activate the poker client window."""

        if self.window:

            try:
                self.window.activate()
                self.window_activation_error_reported = False  # Reset the flag if activation is successful

            except Exception as e:

                if not self.window_activation_error_reported:
                    print(F"{Fore.RED}HeroActions -> Error activating window: {e}")
                    self.window_activation_error_reported = True
        else:

            if not self.window_activation_error_reported:
                print(F"{Fore.RED}HeroActions -> Window not located or cannot be activated.")
                self.window_activation_error_reported = True

