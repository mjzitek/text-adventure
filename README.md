# Post-Apocalyptic Text Adventure Game

A console-based, text-driven adventure game powered by OpenAI's LLM. Set in a post-apocalyptic world ravaged by climate disaster, this game offers a dynamic storytelling experience that adapts to your choices and remembers your decisions.

## Features

- Character creation with backgrounds and personality traits
- Dynamic storytelling powered by OpenAI's GPT-4o models
- Memory system that tracks your choices and relationships
- NPCs that remember your interactions and evolve based on your decisions
- Inventory system for items you collect during your journey
- Journal to review your adventure progress
- Automatic story logging for revisiting your adventure later
- SQLite database for persistent game state

## Requirements

- Python 3.8+
- OpenAI API key

## Installation

1. Clone this repository:
```
git clone https://github.com/mjzitek/text-adventure.git
cd text-adventure
```

2. Create a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the game:
```
python app/main.py
```

## Game Commands

During gameplay, you can use these commands:
- `I` or `inventory`: Check your inventory
- `J` or `journal`: View your recent events
- `C` or `characters`: See characters you've met
- `H` or `help`: Display help text
- `Q` or `quit`: End the game

## Project Structure

```
text-adventure/
├── app/                  # Main application code
│   ├── main.py           # Game entry point
│   ├── character.py      # Character creation and management
│   ├── story_engine.py   # Core storytelling engine
│   ├── memory.py         # Memory and state tracking
│   ├── db.py             # Database interactions
│   ├── llm.py            # OpenAI API integration
│   ├── input_handler.py  # User input processing
│   └── config.py         # Configuration settings
├── data/                 # Game data and storage
│   ├── prompts/          # LLM prompt templates
│   └── game.db           # SQLite database for game state
├── docs/                 # Documentation
├── requirements.txt      # Dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Customization

You can customize the game by editing the prompt templates in the `data/prompts/` directory:
- `system_prompt.txt`: Sets the overall tone and rules for the LLM
- `character_creation.txt`: Template for character generation
- `story_generation.txt`: Template for story progression

## Game Mechanics

The game features:
- **Branching Narrative**: Your choices affect the story direction
- **Resource Management**: Manage limited supplies in a harsh world
- **NPC Relationships**: Build alliances or make enemies
- **Puzzles and Challenges**: Test your problem-solving skills
- **Persistent World**: The game remembers your actions across sessions

## Future Enhancements

- Multiplayer capabilities
- More extensive world-building
- Additional character classes and backgrounds
- Voice narration options
- Web-based interface

## License

MIT

## Acknowledgements

- OpenAI for the GPT models
- Inspired by classic text adventures and tabletop RPGs
- Built with Python and SQLite 