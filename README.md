# PokerGPT Bot

PokerGPT is an advanced online poker-playing bot for Pokerstars(6-player Texas Holdem, Cash game) that utilizes the OpenAI GPT-4 API for real-time game state analysis and decision-making.

## Features

- Real-time detection of game events by reading pixels on the screen.
- Uses 'gpt-4-1106-preview'
- Uses Tesseract OCR API to recognize cards, pot sizes, dealer button and player actions.
- Advanced GPT-4 prompt engineering for analyzing game states, player exploitation and strategizing.
- Simulates mouse clicks within the poker client for automated gameplay.

## Prerequisites

- Python 3.8 or higher
- Access to OpenAI GPT-4 API
- Tesseract OCR installed for text recognition
- Pokerstars client

## Installation

1. Clone the repository to your local machine.
2. Install the required Python dependencies by running `pip install -r requirements.txt`.
3. Set up your OpenAI API key in the `pokergpt.env` file.
4. Make sure Tesseract OCR is installed and its path is correctly set in the scripts(Tesseract is part of this code).

## Usage

To start the PokerGPT bot, follow these steps:

1. Open Pokerstars client and ensure it's visible on the screen.
2. Run `main.py` to initiate the bot: `python main.py`.
3. Enter your player number (player number starts from bottom and goes clockwise 1, 2, 3, 4, 5, 6)
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

## Contributing

Contributions to PokerGPT are welcome!

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Support

I do not provide any further support for this project. If you can't figure it out, it's not for you.
