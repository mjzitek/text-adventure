"""
Configuration settings for the text adventure game.
"""
import os
from pathlib import Path

class Config:
    """Configuration class for the game."""
    
    def __init__(self):
        # Base paths
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        self.data_dir = self.base_dir / "data"
        self.prompts_dir = self.data_dir / "prompts"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Database
        self.db_path = self.data_dir / "game.db"
        
        # LLM settings
        self.model = "gpt-4o-mini"  # Default model
        self.temperature = 0.7
        self.max_tokens = 500
        
        # Game settings
        self.max_rounds = 20  # Default max rounds for a game
        self.max_history_items = 10  # Max number of history items to keep in memory
        
        # Prompt templates
        self.system_prompt_path = self.prompts_dir / "system_prompt.txt"
        self.character_prompt_path = self.prompts_dir / "character_creation.txt"
        self.story_prompt_path = self.prompts_dir / "story_generation.txt"
        
        # Create default prompt templates if they don't exist
        self._create_default_prompts()
    
    def _create_default_prompts(self):
        """Create default prompt templates if they don't exist."""
        # System prompt
        if not self.system_prompt_path.exists():
            system_prompt = """You are the Game Master for a post-apocalyptic text adventure game set in a world ravaged by climate disaster. 
Your role is to create an immersive, engaging narrative experience for the player.

Follow these guidelines:
1. Create vivid descriptions of the post-apocalyptic world
2. Develop interesting NPCs with distinct personalities
3. Present meaningful choices to the player
4. Maintain consistency with previous events and player choices
5. Adapt the story based on the player's character and decisions
6. Keep the tone consistent with a climate disaster setting

The world is harsh but not without hope. Resources are scarce, and survival is difficult.
Communities have formed, some cooperative, others exploitative.
Nature has been transformed - some areas are barren, others overtaken by mutated flora.

Always end your responses with 2-3 clear options for the player, or prompt them for their next action."""
            
            with open(self.system_prompt_path, 'w') as f:
                f.write(system_prompt)
        
        # Character creation prompt
        if not self.character_prompt_path.exists():
            character_prompt = """Based on the following information about a player character in a post-apocalyptic world after a climate disaster, create a brief character description (2-3 paragraphs).

Name: {name}
Background: {background}
Personality Traits: {traits}

The description should include:
1. How they've survived in this harsh world
2. What skills or knowledge they have from their background
3. How their personality traits influence their approach to survival
4. A hint at what they might be seeking or hoping for in this world

Keep the tone consistent with a climate disaster setting, but allow for personal hope and motivation."""
            
            with open(self.character_prompt_path, 'w') as f:
                f.write(character_prompt)
        
        # Story generation prompt
        if not self.story_prompt_path.exists():
            story_prompt = """Continue the post-apocalyptic adventure with the following context:

Character: {character_description}

Current Situation: {current_situation}

Recent Events:
{recent_events}

NPC Relationships:
{npc_relationships}

Generate the next segment of the story (about 2-3 paragraphs) based on the player's last action: "{player_action}"

Then, present 2-3 clear options for what the player could do next, or ask them what they want to do.

Make sure your response:
1. Acknowledges and builds upon the player's choice
2. Advances the story in a meaningful way
3. Introduces interesting challenges, discoveries, or character interactions
4. Maintains consistency with the established world and previous events
5. Reflects the tone of a climate-disaster post-apocalyptic setting"""
            
            with open(self.story_prompt_path, 'w') as f:
                f.write(story_prompt) 