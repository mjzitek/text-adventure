"""
Story engine module for the text adventure game.
Handles story generation and progression.
"""
import os
import sys
import time
from pathlib import Path

class StoryEngine:
    """Manages story generation and progression."""
    
    def __init__(self, db, llm_client, memory_manager):
        """Initialize the story engine."""
        self.db = db
        self.llm_client = llm_client
        self.memory_manager = memory_manager
        self.current_round = 1
        self.current_game_id = None
        self.current_player = None
        self.story_log = []
    
    def print_slow(self, text, delay=0.03):
        """Print text with a typing effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def start_game(self, player):
        """Start a new game with the given player."""
        self.current_player = player
        self.current_game_id = player.get('game_id')
        self.current_round = 1
        
        # Get the initial story prompt
        template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "story_generation.txt"
        
        # Generate the opening scenario
        opening = self.llm_client.generate_story_segment(
            player.get('description', ''),
            "Starting your journey in the wasteland.",
            [],  # No recent events yet
            [],  # No NPCs yet
            "begin the adventure",
            template_path if template_path.exists() else None
        )
        
        # Update game state
        self.memory_manager.update_game_state(
            self.current_game_id,
            self.current_round,
            "Starting your journey in the wasteland."
        )
        
        # Add the opening as the first event
        self.memory_manager.add_event(
            self.current_game_id,
            self.current_round,
            opening,
            "begin the adventure"
        )
        
        # Extract potential NPCs and items
        self.memory_manager.extract_npcs_from_text(opening, self.current_game_id, self.current_round)
        new_items = self.memory_manager.extract_items_from_text(opening, self.current_game_id)
        
        # Display the opening
        self.print_slow(opening)
        
        # Add to story log
        self.story_log.append({
            "round": self.current_round,
            "text": opening,
            "action": "begin the adventure"
        })
        
        # Notify about new items if any
        if new_items:
            print("\nAdded to inventory: " + ", ".join(new_items))
    
    def process_action(self, action):
        """Process a player action and generate the next story segment."""
        if not self.current_game_id or not self.current_player:
            return "Error: No active game."
        
        # Increment round
        self.current_round += 1
        
        # Get game state
        game_state = self.memory_manager.get_game_state(self.current_game_id)
        current_situation = game_state.get('current_situation', '')
        
        # Get recent events
        recent_events = self.memory_manager.get_recent_events(self.current_game_id)
        
        # Get NPCs
        npcs = self.memory_manager.get_npcs(self.current_game_id)
        
        # Get template path
        template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "story_generation.txt"
        
        # Generate the next story segment
        next_segment = self.llm_client.generate_story_segment(
            self.current_player.get('description', ''),
            current_situation,
            recent_events,
            npcs,
            action,
            template_path if template_path.exists() else None
        )
        
        # Update game state with new situation (use first paragraph as current situation)
        new_situation = next_segment.split('\n\n')[0] if '\n\n' in next_segment else next_segment
        self.memory_manager.update_game_state(
            self.current_game_id,
            self.current_round,
            new_situation
        )
        
        # Add the new segment as an event
        self.memory_manager.add_event(
            self.current_game_id,
            self.current_round,
            next_segment,
            action
        )
        
        # Extract potential NPCs and items
        self.memory_manager.extract_npcs_from_text(next_segment, self.current_game_id, self.current_round)
        new_items = self.memory_manager.extract_items_from_text(next_segment, self.current_game_id)
        
        # Display the story segment
        self.print_slow(next_segment)
        
        # Add to story log
        self.story_log.append({
            "round": self.current_round,
            "text": next_segment,
            "action": action
        })
        
        # Notify about new items if any
        if new_items:
            print("\nAdded to inventory: " + ", ".join(new_items))
        
        return next_segment
    
    def end_game(self, player):
        """End the current game and generate an epilogue."""
        if not self.current_game_id:
            return "No active game to end."
        
        print("\n=== GAME OVER ===\n")
        
        # Generate an epilogue
        recent_events = self.memory_manager.get_recent_events(self.current_game_id, 10)
        
        epilogue_prompt = f"""{player['name']}'s """
        
        system_prompt = ""
        
        epilogue = self.llm_client.generate_text(epilogue_prompt, system_prompt)
        
        # Display the epilogue
        print("\n=== EPILOGUE ===\n")
        self.print_slow(epilogue)
        
        # Save the complete story to a file
        self._save_story_log(player)
        
        return epilogue
    
    def _save_story_log(self, player):
        """Save the complete story to a file."""
        if not self.story_log:
            return
        
        # Create logs directory if it doesn't exist
        logs_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create a filename based on player name and timestamp
        filename = f"{player['name'].lower().replace(' ', '_')}_{int(time.time())}.txt"
        file_path = logs_dir / filename
        
        with open(file_path, 'w') as f:
            f.write(f"=== ADVENTURE LOG: {player['name']} ===\n\n")
            f.write(f"Background: {player['background']}\n")
            f.write(f"Traits: {player['traits']}\n\n")
            f.write(f"{player['description']}\n\n")
            f.write("=== THE JOURNEY ===\n\n")
            
            for entry in self.story_log:
                f.write(f"--- Round {entry['round']} ---\n\n")
                f.write(f"{entry['text']}\n\n")
                f.write(f"Your action: {entry['action']}\n\n")
        
        print(f"\nYour adventure has been saved to: {file_path}")
    
    def get_help_text(self):
        """Get help text for the game."""
        help_text = """
=== GAME HELP ===

COMMANDS:
- I or inventory: Check your inventory
- J or journal: View your recent events
- C or characters: See characters you've met
- H or help: Display this help text
- Q or quit: End the game

GAMEPLAY:
- Type your actions or choices to progress the story
- Be creative with your responses
- Your choices affect the story and relationships

The world is yours to explore. Good luck!
"""
        return help_text 