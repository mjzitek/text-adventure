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

        # Debugging
        print('=' * 40)
        print(messages)
        print('=' * 40)
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                # Debugging
                print('\n\n')
                print('*' * 40)
                print(response.choices[0].message.content)
                print('*' * 40)
                print('\n\n')
                
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
    
    def generate_story_premise(self, character_info, template_path=None):
        """Generate a story premise."""
        template = ""
        
        if template_path and Path(template_path).exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = ""
    
        prompt = template.format(
            character_info=character_info
        )

        system_prompt = "You are a writer who is an expert and creating engaging stories"
        
        return self.generate_text(prompt, system_prompt, temperature=0.7, max_tokens=2000) 


    def summarize_story(self, story_premise, character_description, current_summary, 
                              recent_events, npc_relationships, player_action, 
                              template_path=None):
        """Summarize the story."""
        template = ""
        print("+ Summarize the story. +")
        
        if template_path and isinstance(template_path, str) and Path(template_path).exists():
            print("+ Template path exists. +")
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = """
Summarize the story so far, incorporating the recent events. Create a cohesive narrative that captures the key elements of the story.

Story Premise:
{story_premise}

Character Description:
{character_description}

Current Summary:
{current_summary}

Recent Events:
{recent_events}

NPC Relationships:
{npc_relationships}

Latest Player Action:
{player_action}

Create a comprehensive summary of the story so far:
"""

        # Format recent events
        events_text = ""
        if recent_events:
            for event in recent_events:
                # Make sure we're handling dictionary items properly
                round_num = event.get('round', 'unknown')
                description = event.get('description', '')
                player_action = player_action
                
                # Use the first paragraph of the description if it's too long
                # if description and '\n\n' in description:
                #     description = description.split('\n\n')[0]
                
                events_text += f"\n**********\n **Round {round_num}:**\n {description} (Player Choice: {player_action})\n"
        else:
            events_text = "No previous events."
        
        # Format NPC relationships
        npcs_text = ""
        if npc_relationships:
            for npc in npc_relationships:
                # Make sure we're handling dictionary items properly
                name = npc.get('name', 'Unknown')
                relationship = npc.get('relationship', 'neutral')
                description = npc.get('description', '')
                
                npcs_text += f"- {name}: {relationship} - {description}\n"
        else:
            npcs_text = "No established NPC relationships yet."
        
        prompt = template.format(
            story_premise=story_premise,
            character_description=character_description,
            current_summary=current_summary or "The story is just beginning.",
            recent_events=events_text,
            npc_relationships=npcs_text,
            player_action=player_action,
            latest_events=events_text
        )
        
        system_prompt = "You are a writer who is an expert at summarizing complex narratives in a concise and engaging way."
        
        return self.generate_text(prompt, system_prompt, temperature=0.7, max_tokens=1000)

    def generate_story_segment(self, story_premise, character_description, current_situation, 
                              recent_events, npc_relationships, player_action, 
                              template_path=None):
        """Generate a story segment."""
        template = ""
        print("+ Generate a story segment. +")
        print ("+ Story premise: " + story_premise[:30] if story_premise else "") # First 10 chars or empty string
        print ("+ Character info: " + character_description[:30] if character_description else "") # First 10 chars or empty string
        #print ("+ Current situation: " + current_situation[:10] if current_situation else "") # First 10 chars or empty string
        
        # Properly handle arrays of dictionaries
        if recent_events:
            print(f"+ Recent events: {len(recent_events)} events")
        else:
            print("+ Recent events: None")
            
        if npc_relationships:
            print(f"+ NPC relationships: {len(npc_relationships)} NPCs")
        else:
            print("+ NPC relationships: None")
            
        print ("+ Player action: " + player_action[:40] if player_action else "") # First 10 chars or empty string
        
        # Ensure template_path is a string
        if template_path and isinstance(template_path, str) and Path(template_path).exists():
            with open(template_path, 'r') as f:
                template = f.read()
        else:
            template = ""

        # Format recent events
        events_text = ""
        if recent_events:
            for event in recent_events:
                # Make sure we're handling dictionary items properly
                round_num = event.get('round', 'unknown')
                description = event.get('description', '')
                player_choice = event.get('player_action', '')
                
                # Use the first paragraph of the description if it's too long
                # if description and '\n\n' in description:
                #     description = description.split('\n\n')[0]
                
                events_text += f"\n**********\n **Round {round_num}:**\n {description} \n Player Choice: {player_choice}\n"
        else:
            events_text = "No previous events."
        
        # Format NPC relationships
        npcs_text = ""
        if npc_relationships:
            for npc in npc_relationships:
                # Make sure we're handling dictionary items properly
                name = npc.get('name', 'Unknown')
                relationship = npc.get('relationship', 'neutral')
                description = npc.get('description', '')
                
                npcs_text += f"- {name}: {relationship} - {description}\n"
        else:
            npcs_text = "No established NPC relationships yet."
        
        prompt = template.format(
            character_info=character_description,
            story_premise=story_premise,
            summary=current_situation or "Starting your journey in the wasteland.",
            recent_events=events_text,
            npc_relationships=npcs_text,
            player_response=player_action
        )
        
        # Read system prompt if available
        system_prompt = ""
        system_prompt_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "system_prompt.txt"
        
        if system_prompt_path.exists():
            with open(system_prompt_path, 'r') as f:
                system_prompt = f.read()
        
        return self.generate_text(prompt, system_prompt, temperature=0.7, max_tokens=2000) 