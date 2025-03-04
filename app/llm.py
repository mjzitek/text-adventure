"""
LLM client module for OpenAI integration.
"""
import os
import time
from openai import OpenAI
from pathlib import Path

class LLMClient:
    """Client for interacting with OpenAI's LLM."""
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """Initialize the LLM client."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_text(self, prompt, system_prompt=None, temperature=0.7, max_tokens=500):
        """Generate text using the LLM."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        # Retry mechanism for API calls
        max_retries = 3
        retry_delay = 2

        print(messages)
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                print(response.choices[0].message.content)
                
                return response.choices[0].message.content
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error calling OpenAI API: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"Failed to generate text after {max_retries} attempts: {e}")
                    return "I'm having trouble connecting to my storytelling abilities right now. Please try again."
    
    def generate_character_description(self, name, gender, background, traits, template_path=None):
        """Generate a character description."""
        template = ""
        
        if template_path and Path(template_path).exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = """"""
        
        prompt = template.format(
            name=name,
            gender=gender,
            background=background,
            traits=traits
        )
        print(prompt)
        
        system_prompt = "You are a writer who is an expert and creating engaging stories"
        
        return self.generate_text(prompt, system_prompt)
    
    def generate_story_segment(self, character_description, current_situation, 
                              recent_events, npc_relationships, player_action, 
                              template_path=None):
        """Generate a story segment."""
        template = ""
        
        if template_path and Path(template_path).exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = """
    
"""
        
        # Format recent events
        events_text = ""
        if recent_events:
            for event in recent_events:
                events_text += f"- Round {event.get('round')}: {event.get('description')} (Player: {event.get('player_action')})\n"
        else:
            events_text = "No previous events."
        
        # Format NPC relationships
        npcs_text = ""
        if npc_relationships:
            for npc in npc_relationships:
                npcs_text += f"- {npc.get('name')}: {npc.get('relationship')} - {npc.get('description')}\n"
        else:
            npcs_text = "No established NPC relationships yet."
        
        prompt = template.format(
            character_description=character_description,
            current_situation=current_situation or "Starting your journey in the wasteland.",
            recent_events=events_text,
            npc_relationships=npcs_text,
            player_action=player_action
        )
        
        # Read system prompt if available
        system_prompt = ""
        system_prompt_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "system_prompt.txt"
        
        if system_prompt_path.exists():
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read()
        
        return self.generate_text(prompt, system_prompt, temperature=0.7, max_tokens=800) 