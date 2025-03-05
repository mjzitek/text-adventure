#!/usr/bin/env python3
"""
Text Adventure Game - Main Entry Point
A post-apocalyptic text adventure game powered by LLM.
"""
import os
import sys
import time
from dotenv import load_dotenv

from config import Config
from character import CharacterManager
from story_engine import StoryEngine
from memory import MemoryManager
from input_handler import InputHandler
from llm import LLMClient
from db import Database
from text_formatter import bold, colored, CYAN, YELLOW, format_story_text, format_markdown

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text, delay=0.03):
    """Print text with a typing effect."""
    # Make sure text is a string
    if not isinstance(text, str):
        text = str(text)
        
    # Apply text formatting
    formatted_text = format_markdown(text)
    
    for char in formatted_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_title():
    """Display the game title."""
    clear_screen()
    title = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   POST-APOCALYPTIC CHRONICLES: ECHOES OF THE NEW WORLD     ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    # Print the title with cyan color
    print(colored(title, CYAN))
    print_slow(bold("In a world ravaged by climate disaster, your story begins...") + "\n")
    time.sleep(1)

def main():
    """Main game function."""
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    config = Config()
    db = Database(config.db_path)
    llm_client = LLMClient(api_key=os.getenv("OPENAI_API_KEY"))
    memory_manager = MemoryManager(db)
    character_manager = CharacterManager(db, llm_client)
    story_engine = StoryEngine(db, llm_client, memory_manager)
    input_handler = InputHandler(story_engine, memory_manager)
    
    # Display title
    display_title()
    
    # Character creation
    player = character_manager.create_character()
    
    # Start the game
    story_engine.start_game(player)
    
    # Main game loop
    game_active = True
    while game_active:
        # Get player input
        user_input = input("\n> ").strip()
        
        # Process input
        result = input_handler.process_input(user_input, player)
        
        # Check if game should end
        if result.get("end_game", False):
            game_active = False
        # Skip to next iteration if the input was invalid
        elif result.get("type") == "invalid_choice":
            print(colored("Please enter 1, 2, or 3 to select one of the available choices.", YELLOW))
            continue
    
    # End game
    story_engine.end_game(player)
    print_slow("\nThank you for playing!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame terminated. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1) 