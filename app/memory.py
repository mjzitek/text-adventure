"""
Memory management module for the text adventure game.
Handles game state and memory tracking.
"""

class MemoryManager:
    """Manages game state and memory."""
    
    def __init__(self, db):
        """Initialize the memory manager."""
        self.db = db
    
    def get_game_state(self, game_id):
        """Get the current game state."""
        return self.db.get_game_state(game_id)
    
    def update_game_state(self, game_id, current_round=None, current_situation=None):
        """Update the game state."""
        self.db.update_game_state(game_id, current_round, current_situation)
    
    def add_event(self, game_id, round_num, description, player_action):
        """Add a new event to the game history."""
        self.db.add_event(game_id, round_num, description, player_action)
    
    def get_recent_events(self, game_id, limit=5):
        """Get recent events from the game history."""
        return self.db.get_recent_events(game_id, limit)
    
    def add_npc(self, game_id, name, description, relationship="neutral", first_met_round=1):
        """Add a new NPC to the game."""
        self.db.add_npc(game_id, name, description, relationship, first_met_round)
    
    def update_npc(self, npc_id, description=None, relationship=None):
        """Update an NPC's information."""
        self.db.update_npc(npc_id, description, relationship)
    
    def get_npcs(self, game_id):
        """Get all NPCs for a game."""
        return self.db.get_npcs(game_id)
    
    def update_inventory(self, game_id, items):
        """Update the player's inventory."""
        self.db.update_inventory(game_id, items)
    
    def get_inventory(self, game_id):
        """Get the player's inventory."""
        return self.db.get_inventory(game_id)
    
    def extract_npcs_from_text(self, text, game_id, current_round):
        """Extract potential NPCs from story text and add them to the database."""
        # This is a simple implementation that could be enhanced with NLP
        # For now, we'll look for common NPC indicators in the text
        
        lines = text.split('\n')
        potential_npcs = []
        
        # Look for dialogue indicators or name patterns
        for line in lines:
            if '"' in line or "'" in line:
                # Look for patterns like "Name: dialogue" or "Name said"
                parts = line.split('"')[0].split("'")[0].strip()
                if ':' in parts:
                    name = parts.split(':')[0].strip()
                    if name and len(name) < 20 and name.lower() not in ['you', 'i', 'we', 'they']:
                        potential_npcs.append(name)
                
                for word in ['says', 'said', 'asked', 'replied', 'shouted', 'whispered']:
                    if word in parts:
                        name_parts = parts.split(word)[0].strip().split()
                        if name_parts and name_parts[-1].lower() not in ['you', 'i', 'we', 'they']:
                            potential_npcs.append(name_parts[-1])
        
        # Get existing NPCs
        existing_npcs = self.get_npcs(game_id)
        existing_names = [npc['name'].lower() for npc in existing_npcs]
        
        # Add new NPCs
        for npc_name in potential_npcs:
            if npc_name.lower() not in existing_names:
                self.add_npc(
                    game_id,
                    npc_name,
                    f"Met during round {current_round}",
                    "neutral",
                    current_round
                )
    
    def extract_items_from_text(self, text, game_id):
        """Extract potential items from story text and add them to inventory."""
        # This is a simple implementation that could be enhanced with NLP
        # For now, we'll look for common item indicators in the text
        
        # Get current inventory
        current_inventory = self.get_inventory(game_id)
        
        # Look for phrases like "you found a [item]" or "you picked up [item]"
        item_indicators = [
            "found a ", "found an ", "picked up a ", "picked up an ",
            "discovered a ", "discovered an ", "obtained a ", "obtained an ",
            "received a ", "received an ", "given a ", "given an "
        ]
        
        new_items = []
        lower_text = text.lower()
        
        for indicator in item_indicators:
            if indicator in lower_text:
                parts = lower_text.split(indicator)
                for i in range(1, len(parts)):
                    item_part = parts[i].split(".")[0].split(",")[0].split("\n")[0]
                    if item_part and len(item_part) < 30:
                        item = item_part.strip()
                        if item and item not in current_inventory and item not in new_items:
                            new_items.append(item)
        
        # Update inventory if new items were found
        if new_items:
            updated_inventory = current_inventory + new_items
            self.update_inventory(game_id, updated_inventory)
            
            return new_items
        
        return []
    
    def format_recent_events(self, game_id, limit=5):
        """Format recent events for display."""
        events = self.get_recent_events(game_id, limit)
        if not events:
            return "No events recorded yet."
        
        formatted = "\n=== RECENT EVENTS ===\n"
        for event in reversed(events):  # Show most recent last
            formatted += f"\nRound {event['round']}:\n"
            formatted += f"{event['description']}\n"
            formatted += f"Your action: {event['player_action']}\n"
        
        return formatted
    
    def format_inventory(self, game_id):
        """Format inventory for display."""
        items = self.get_inventory(game_id)
        
        if not items:
            return "Your inventory is empty."
        
        formatted = "\n=== INVENTORY ===\n"
        for i, item in enumerate(items, 1):
            formatted += f"{i}. {item}\n"
        
        return formatted
    
    def format_npcs(self, game_id):
        """Format NPCs for display."""
        npcs = self.get_npcs(game_id)
        
        if not npcs:
            return "You haven't met any notable characters yet."
        
        formatted = "\n=== CHARACTERS YOU'VE MET ===\n"
        for npc in npcs:
            formatted += f"\n{npc['name']} ({npc['relationship']})\n"
            formatted += f"{npc['description']}\n"
        
        return formatted 