import datetime
import pygame
import queue
from pathlib import Path

class AudioPlayer:

    def __init__(self, openai_client):

        pygame.mixer.init()

        self.client             = openai_client

        self.audio_base_path    = 'Audio/'                              # Set the path to the audio files directory

        self.audio_queue        = queue.Queue()                         # Queue to hold audio files

        self.is_playing         = False                                 # Flag to check if an audio is currently being played

        self.sound_active       = True                                  # Set to False if you don't want to play any voiceovers.


    def add_to_queue(self, file_name):

        # Add an audio file to the queue
        self.audio_queue.put(file_name)
        self.play_next_audio()


    def play_next_audio(self):
        
        if self.sound_active is False:
            return
        
        # Play the next audio file in the queue
        if not self.audio_queue.empty() and not self.is_playing:
            file_name = self.audio_queue.get()
            pygame.mixer.music.load(self.audio_base_path + file_name)
            pygame.mixer.music.play()
            self.is_playing = True
            while pygame.mixer.music.get_busy():  # Wait for the audio to finish playing
                pygame.time.Clock().tick(10)
            self.is_playing = False
            self.play_next_audio()  # Play the next audio in the queue


    def convert_text_to_speech(self, text):
        
        if self.sound_active is False:
            return
        
        print("Converting text to speech...")

        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        # Generate a timestamp for the file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        speech_file_name = f"GPT4_Analysis_Result_{timestamp}.mp3"

        # Path for the speech audio file with timestamp
        speech_file_path = Path(self.audio_base_path +"GPT_Analysis/"+speech_file_name)

        # Save the new speech audio to a file
        with open(speech_file_path, "wb") as f:
            f.write(response.read())
        
        #print("Speech file saved.")
        final_return_audio_path = "GPT_Analysis/"+speech_file_name

        return final_return_audio_path
    

    def play_speech(self, text):

        # Convert text to speech and get the file path
        speech_file_path = self.convert_text_to_speech(text)

        # Add the speech file to the queue
        self.add_to_queue(str(speech_file_path))


    # Player actions Audio
    def play_bet_audio(self, player_number):
        file_name = f'Player_Bet/Player_{player_number}_Bet.mp3'
        self.add_to_queue(file_name)

    def play_call_audio(self, player_number):
        file_name = f'Player_Call/Player_{player_number}_Call.mp3'
        self.add_to_queue(file_name)

    def play_fold_audio(self, player_number):
        file_name = f'Player_Fold/Player_{player_number}_Fold.mp3'
        self.add_to_queue(file_name)

    def play_is_dealer_audio(self, player_number):
        file_name = f'Player_is_Dealer/Player_{player_number}_is_the_dealer.mp3'
        self.add_to_queue(file_name)

    def play_raise_audio(self, player_number):
        file_name = f'Player_Raise/Player_{player_number}_Raise.mp3'
        self.add_to_queue(file_name)

    def play_check_audio(self, player_number):
        file_name = f'Player_Check/Player_{player_number}_Check.mp3'
        self.add_to_queue(file_name)

    def play_left_audio(self, player_number):
        file_name = f'Player_Left/Player_{player_number}_left.mp3'
        self.add_to_queue(file_name)

    def play_wins_the_pot_audio(self, player_number):
        file_name = f'Player_wins_pot/Player_{player_number}_wins_the_pot.mp3'
        self.add_to_queue(file_name)

    def play_turn_audio(self, player_number):
        file_name = f'Player_Turn/Player_{player_number}_Turn.mp3'
        self.add_to_queue(file_name)


    # Audio for Board Stage
    def play_board_flop_audio(self):
        self.add_to_queue('Board_Stage/Flop.mp3')

    def play_new_round_started_audio(self):
        self.add_to_queue('Board_Stage/New_round_started.mp3')

    def play_board_pre_flop_audio(self):
        self.add_to_queue('Board_Stage/Pre_flop.mp3')

    def play_board_river_audio(self):
        self.add_to_queue('Board_Stage/River.mp3')

    def play_board_turn_audio(self):
        self.add_to_queue('Board_Stage/Turn.mp3')


    # Audio for Hero Player
    def play_hero_is_big_blind_audio(self):
        self.add_to_queue('Hero/Hero_is_big_blind.mp3')

    def play_hero_is_small_blind_audio(self):
        self.add_to_queue('Hero/Hero_is_small_blind.mp3')

    def play_hero_is_the_dealer_audio(self):
        self.add_to_queue('Hero/Hero_is_the_dealer.mp3')

    def play_hero_lost_the_hand_audio(self):
        self.add_to_queue('Hero/Hero_lost_the_hand.mp3')

    def play_your_turn_audio(self):
        self.add_to_queue('Hero/Your_turn.mp3')
