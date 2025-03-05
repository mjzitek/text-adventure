"""
Story engine module for the text adventure game.
Handles story generation and progression.
"""
import os
import sys
import time
from pathlib import Path

from text_formatter import format_story_text, bold, colored, underline, CYAN, GREEN, YELLOW, RED

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
    
    def print_slow(self, text, delay=0.00):
        """Print text with a typing effect."""
        # Make sure text is a string
        if not isinstance(text, str):
            text = str(text)
            
        # Apply text formatting before printing
        formatted_text = format_story_text(text)
        for char in formatted_text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def start_game(self, player):
        """Start a new game with the given player."""
        self.current_player = player
        self.current_game_id = player.get('game_id')
        self.current_round = 1
        
        premise_template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "story_premise.txt"
        story_template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "story_generation.txt"
        
        
        # Generate the opening scenario
        opening = self.llm_client.generate_story_premise(
            player.get('description', ''),
            premise_template_path if premise_template_path.exists() else None
        )
        
        # Display the opening
        self.print_slow(opening)
        
        # Add to story log
        self.story_log.append({
            "round": self.current_round,
            "text": opening,
            "action": "begin the adventure"
        })
        
        # Update game state with story premise
        self.memory_manager.update_game_state(
            self.current_game_id,
            self.current_round,
            opening,  # current_situation
            opening,  # story_premise
            opening   # initial summary
        )
        
        print('\n** Generating story segment **\n')
        start = self.llm_client.generate_story_segment(
            opening,                                    # story_premise
            player.get('description', ''),              # character_description
            opening,                                    # current_situation
            [],                                         # recent_events
            [],                                         # npc_relationships
            "begin the adventure",                      # player_action
            str(story_template_path) if story_template_path.exists() else None
        )

        self.print_slow(start)

        # Update game state
        self.memory_manager.update_game_state(
            self.current_game_id,
            self.current_round,
            start
        )
    
        self.memory_manager.add_event(
            self.current_game_id,
            self.current_round,
            start,
            "begin the adventure"
        )
        
        # Extract potential NPCs and items
        self.memory_manager.extract_npcs_from_text(opening, self.current_game_id, self.current_round)
        new_items = self.memory_manager.extract_items_from_text(opening, self.current_game_id)
        

        # Notify about new items if any
        if new_items:
            print("\nAdded to inventory: " + ", ".join(new_items))
    
    def process_action(self, action):
        """Process a player action and generate the next story segment."""
        if not self.current_game_id or not self.current_player:
            return "Error: No active game."
        
        print("\n\n$$$$ Action: " + action)

        # Increment round
        self.current_round += 1
        
        # Get game state
        game_state = self.memory_manager.get_game_state(self.current_game_id)
        current_situation = game_state.get('current_situation', '')
        story_premise = game_state.get('story_premise', '')
        current_summary = game_state.get('current_summary', '')
        
        # Get recent events
        recent_events = self.memory_manager.get_recent_events(self.current_game_id)
        
        # Get NPCs
        npcs = self.memory_manager.get_npcs(self.current_game_id)
        
        # Get template path
        template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "story_generation.txt"
        summary_template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "summary.txt"

        # Generate the next story segment
        next_segment = self.llm_client.generate_story_segment(
            story_premise,                              # story_premise
            self.current_player.get('description', ''), # character_description
            current_situation,                          # current_situation
            recent_events,                              # recent_events
            npcs,                                       # npc_relationships
            action,                                     # player_action
            str(template_path) if template_path.exists() else None
        )
        
        print("\n\n$$$$ Next segment:\n")
        print(next_segment)
        print("\n$$$$\n")

        # Summarize the story
        summary = self.llm_client.summarize_story(
            story_premise,
            self.current_player.get('description', ''),
            current_summary,
            recent_events,
            npcs,
            action,
            str(summary_template_path) if summary_template_path.exists() else None
        )

        print("\n\n$$$$ Summary:\n")
        print(summary)
        print("\n$$$$\n")

        # Update game state with new situation and summary
        self.memory_manager.update_game_state(
            self.current_game_id,
            self.current_round,
            next_segment,
            story_premise,  # Preserve the story premise
            summary         # Update the summary
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
        help_text = f"""
{bold(colored('=== GAME HELP ===', CYAN))}

{bold(colored('COMMANDS:', YELLOW))}
- {bold('I')} or {bold('inventory')}: Check your inventory
- {bold('J')} or {bold('journal')}: View your recent events
- {bold('C')} or {bold('characters')}: See characters you've met
- {bold('H')} or {bold('help')}: Display this help text
- {bold('Q')} or {bold('quit')}: End the game

{bold(colored('GAMEPLAY:', YELLOW))}
- Type your actions or choices to progress the story
- Be creative with your responses
- Your choices affect the story and relationships

{colored('The world is yours to explore. Good luck!', GREEN)}
"""
        return help_text 