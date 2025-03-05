"""
Input handler module for the text adventure game.
Processes player input and commands.
"""
from text_formatter import bold, colored, underline, CYAN, GREEN, YELLOW, RED
import re

class InputHandler:
    """Handles player input and commands."""
    
    def __init__(self, story_engine, memory_manager):
        """Initialize the input handler."""
        self.story_engine = story_engine
        self.memory_manager = memory_manager
        self.commands = {
            'i': self._show_inventory,
            'inventory': self._show_inventory,
            'j': self._show_journal,
            'journal': self._show_journal,
            'c': self._show_characters,
            'characters': self._show_characters,
            'h': self._show_help,
            'help': self._show_help,
            'q': self._quit_game,
            'quit': self._quit_game,
            'exit': self._quit_game
        }
        # Flag to track if we're expecting a choice input (1, 2, or 3)
        self.expecting_choice = True
        
        # Set the reference in the story engine
        story_engine.set_input_handler(self)
    
    def process_input(self, user_input, player):
        """Process player input."""
        # Check if input is a command
        command = user_input.lower()
        
        if command in self.commands:
            return self.commands[command](player)
        
        # If we're expecting a choice and the input is not a valid choice (1, 2, or 3),
        # prompt the user to enter a valid choice
        if self.expecting_choice and not self._is_valid_choice(user_input):
            return {"type": "invalid_choice"}
        
        # If not a command, treat as a story action
        # If it was a valid choice (1, 2, or 3), we'll pass just that number to the story engine
        return {
            "type": "story_action",
            "result": self.story_engine.process_action(user_input)
        }
    
    def _is_valid_choice(self, user_input):
        """Check if the user input is a valid choice (1, 2, or 3)."""
        # Strip whitespace and check if the input is exactly "1", "2", or "3"
        stripped_input = user_input.strip()
        return stripped_input in ["1", "2", "3"]
    
    def _show_inventory(self, player):
        """Show the player's inventory."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": colored("No active game.", RED)}
        
        inventory = self.memory_manager.get_inventory(game_id)
        
        # Format inventory with colors and styling
        inventory_text = f"\n{bold(colored('=== INVENTORY ===', CYAN))}\n\n"
        
        if not inventory:
            inventory_text += "Your inventory is empty.\n"
        else:
            for item in inventory:
                inventory_text += f"• {colored(item, GREEN)}\n"
        
        print(inventory_text)
        
        return {"type": "inventory", "result": inventory_text}
    
    def _show_journal(self, player):
        """Show the player's recent events."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": colored("No active game.", RED)}
        
        events = self.memory_manager.get_recent_events(game_id, 10)
        
        # Format journal with colors and styling
        journal_text = f"\n{bold(colored('=== RECENT EVENTS ===', CYAN))}\n\n"
        
        if not events:
            journal_text += "No events recorded yet.\n"
        else:
            for i, event in enumerate(events, 1):
                round_num = event.get('round', i)
                text = event.get('text', '').split('\n\n')[0]  # Get first paragraph
                action = event.get('action', '')
                
                journal_text += f"{bold(colored(f'Round {round_num}:', YELLOW))}\n"
                journal_text += f"{text}\n"
                journal_text += f"{underline('Your action:')} {action}\n\n"
        
        print(journal_text)
        
        return {"type": "journal", "result": journal_text}
    
    def _show_characters(self, player):
        """Show the characters the player has met."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": colored("No active game.", RED)}
        
        npcs = self.memory_manager.get_npcs(game_id)
        
        # Format characters with colors and styling
        characters_text = f"\n{bold(colored('=== CHARACTERS ===', CYAN))}\n\n"
        
        if not npcs:
            characters_text += "You haven't met any notable characters yet.\n"
        else:
            for npc in npcs:
                name = npc.get('name', 'Unknown')
                description = npc.get('description', '')
                
                characters_text += f"{bold(colored(name, GREEN))}\n"
                characters_text += f"{description}\n\n"
        
        print(characters_text)
        
        return {"type": "characters", "result": characters_text}
    
    def _show_help(self, player):
        """Show help text."""
        help_text = self.story_engine.get_help_text()
        print(help_text)
        
        return {"type": "help", "result": help_text}
    
    def _quit_game(self, player):
        """Quit the game."""
        print(f"\n{colored('Are you sure you want to end your adventure? (y/n)', YELLOW)}")
        confirm = input("> ").lower().startswith('y')
        
        if confirm:
            return {"type": "quit", "end_game": True}
        else:
            print(f"\n{colored('Adventure continues...', GREEN)}\n")
            return {"type": "continue"} 