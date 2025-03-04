"""
Input handler module for the text adventure game.
Processes player input and commands.
"""

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
    
    def process_input(self, user_input, player):
        """Process player input."""
        # Check if input is a command
        command = user_input.lower()
        
        if command in self.commands:
            return self.commands[command](player)
        
        # If not a command, treat as a story action
        return {
            "type": "story_action",
            "result": self.story_engine.process_action(user_input)
        }
    
    def _show_inventory(self, player):
        """Show the player's inventory."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": "No active game."}
        
        inventory_text = self.memory_manager.format_inventory(game_id)
        print(inventory_text)
        
        return {"type": "inventory", "result": inventory_text}
    
    def _show_journal(self, player):
        """Show the player's recent events."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": "No active game."}
        
        journal_text = self.memory_manager.format_recent_events(game_id)
        print(journal_text)
        
        return {"type": "journal", "result": journal_text}
    
    def _show_characters(self, player):
        """Show the characters the player has met."""
        game_id = player.get('game_id')
        if not game_id:
            return {"type": "error", "result": "No active game."}
        
        characters_text = self.memory_manager.format_npcs(game_id)
        print(characters_text)
        
        return {"type": "characters", "result": characters_text}
    
    def _show_help(self, player):
        """Show help text."""
        help_text = self.story_engine.get_help_text()
        print(help_text)
        
        return {"type": "help", "result": help_text}
    
    def _quit_game(self, player):
        """Quit the game."""
        print("\nAre you sure you want to end your adventure? (y/n)")
        confirm = input("> ").lower().startswith('y')
        
        if confirm:
            return {"type": "quit", "end_game": True}
        else:
            print("\nAdventure continues...\n")
            return {"type": "continue"} 