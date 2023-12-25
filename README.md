# PokerGPT - GPT4 poker bot for Pokerstars

PokerGPT is an advanced online poker-playing bot for Pokerstars(6-player Texas Hold'em, Cash game) that utilizes the OpenAI GPT-4 API for real-time game state analysis and decision-making.
It has built-in GUI to visualize poker data + voice support to playback actions on the table.

## Features

- Real-time detection of game events by reading pixels on the screen.
- Uses Tesseract OCR API to recognize cards, pot sizes, dealer button and all player actions.
- Uses 'gpt-4-1106-preview' to analyze the game data and players in order to take appriopriate action(fold, check, raise, bet etc).
- Advanced GPT-4 prompt engineering for analyzing game states, player exploitation and strategizing.
- Simulates mouse clicks within the Pokerstars client for automated gameplay.

## Prerequisites

- Python 3.8 or higher
- Access to OpenAI GPT-4 API 
- Tesseract OCR installed for text recognition
- Pokerstars client

## Installation

1. Clone the repository to your local machine.
2. Install the required Python dependencies by running `pip install -r requirements.txt`.
3. Set up your OpenAI API key in the `pokergpt.env` file. (register free account at https://openai.com/ and get your API key here: https://platform.openai.com/api-keys)
4. Make sure Tesseract OCR is installed and its path is correctly set in the scripts(Tesseract is part of this code).

## PokerStars client (Visual) setup:
1. Since this bot reads all of the data from the poker client window, you will need to setup the visuals excactly like in this image:
![PokerTable2](https://github.com/HarperJonesGPT/PokerGPT/assets/154810617/ba0a7bc5-d2d1-4237-bfd8-015ca2ca14e9)
2.Disable all animations for Pokerstars client in the table settings.

## Usage

To start the PokerGPT, follow these steps:

1. Open Pokerstars client and ensure it's visible on the screen.
2. Run `main.py` to initiate the bot: `python main.py`.
3. Enter your own player number (player numbers start from the bottom of the table and goes clockwise 1(bottom), 2(bottom-left), 3(top-eft), 4(top), 5(top-right), 6(bottom-right))
4. The bot will automatically locate the poker window and start playing based on the GPT-4 strategy analysis.


## Structure

- `audio_player.py`: Handles audio feedback from the bot.
- `game_state.py`: Manages the current state of the game.
- `gui.py`: Provides a graphical user interface for monitoring the bot's actions.
- `hero_action.py`: Contains logic for determining the hero's actions.
- `hero_hand_range.py`: Assesses hand ranges for the hero.
- `hero_info.py`: Collects information about the hero's current state.
- `main.py`: Entry point for running the bot.
- `poker_assistant.py`: Interfaces with OpenAI's API to analyze the game state and decide on actions.
- `read_poker_table.py`: Uses OCR and pixel detection to read the table state.

## Limitations
- Dependant on the Pokerstars client window size (PokerGPT automatically resizes to small window)
- Might not work on all screen resolutions (tested on '1920 x 1080' pixel screen resolution, Windows 11)
- Works only in Pokerstars 6-Player table.
- 

## Contributing

Contributions to PokerGPT are welcome!

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Support

I do not provide any further support for this project. If you can't figure it out, it's not for you.
