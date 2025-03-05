"""
Database module for the text adventure game.
Handles database operations and schema.
"""
import sqlite3
import json
from pathlib import Path

class Database:
    """Database manager for the game."""
    
    def __init__(self, db_path):
        """Initialize the database."""
        self.db_path = db_path
        self._create_tables()
        self._add_story_premise_column()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Player table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            background TEXT NOT NULL,
            traits TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Game state table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_state (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            current_round INTEGER DEFAULT 1,
            current_situation TEXT,
            story_premise TEXT,
            current_summary TEXT,
            FOREIGN KEY (player_id) REFERENCES player(id)
        )
        ''')
        
        # Events table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            round INTEGER,
            description TEXT,
            player_action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES game_state(id)
        )
        ''')
        
        # NPCs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS npcs (
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            name TEXT,
            description TEXT,
            relationship TEXT DEFAULT 'neutral',
            first_met_round INTEGER,
            FOREIGN KEY (game_id) REFERENCES game_state(id)
        )
        ''')
        
        # Inventory table (simple)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            items TEXT,  -- JSON string of items
            FOREIGN KEY (game_id) REFERENCES game_state(id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def _add_story_premise_column(self):
        """Add story_premise column to game_state table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if story_premise column exists in game_state table
        cursor.execute("PRAGMA table_info(game_state)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add story_premise column if it doesn't exist
        if 'story_premise' not in columns:
            print("Adding story_premise column to game_state table")
            cursor.execute("ALTER TABLE game_state ADD COLUMN story_premise TEXT")
            conn.commit()
            
        # Add current_summary column if it doesn't exist
        if 'current_summary' not in columns:
            print("Adding current_summary column to game_state table")
            cursor.execute("ALTER TABLE game_state ADD COLUMN current_summary TEXT")
            conn.commit()
        
        conn.close()
    
    def create_player(self, name, background, traits, description=None):
        """Create a new player character."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO player (name, background, traits, description) VALUES (?, ?, ?, ?)",
            (name, background, traits, description)
        )
        player_id = cursor.lastrowid
        
        # Create initial game state
        cursor.execute(
            "INSERT INTO game_state (player_id) VALUES (?)",
            (player_id,)
        )
        game_id = cursor.lastrowid
        
        # Create empty inventory
        cursor.execute(
            "INSERT INTO inventory (game_id, items) VALUES (?, ?)",
            (game_id, json.dumps([]))
        )
        
        conn.commit()
        conn.close()
        
        return self.get_player(player_id)
    
    def get_player(self, player_id):
        """Get player data by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM player WHERE id = ?", (player_id,))
        player = dict(cursor.fetchone())
        
        cursor.execute("SELECT id FROM game_state WHERE player_id = ?", (player_id,))
        game_state = cursor.fetchone()
        if game_state:
            player['game_id'] = game_state['id']
        
        conn.close()
        return player
    
    def update_game_state(self, game_id, current_round=None, current_situation=None, story_premise=None, current_summary=None):
        """Update the game state."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if current_round is not None:
            updates.append("current_round = ?")
            params.append(current_round)
        
        if current_situation is not None:
            updates.append("current_situation = ?")
            params.append(current_situation)
            
        if story_premise is not None:
            updates.append("story_premise = ?")
            params.append(story_premise)
            
        if current_summary is not None:
            updates.append("current_summary = ?")
            params.append(current_summary)
        
        if updates:
            query = f"UPDATE game_state SET {', '.join(updates)} WHERE id = ?"
            params.append(game_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def get_game_state(self, game_id):
        """Get the current game state."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM game_state WHERE id = ?", (game_id,))
        row = cursor.fetchone()
        
        if row:
            state = dict(row)
        else:
            state = {
                "id": game_id, 
                "current_round": 1, 
                "current_situation": "", 
                "story_premise": "",
                "current_summary": ""
            }
        
        conn.close()
        return state
    
    def add_event(self, game_id, round_num, description, player_action):
        """Add a new event to the game history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO events (game_id, round, description, player_action) VALUES (?, ?, ?, ?)",
            (game_id, round_num, description, player_action)
        )
        
        conn.commit()
        conn.close()
    
    def get_recent_events(self, game_id, limit=5):
        """Get recent events from the game history."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM events WHERE game_id = ? ORDER BY round ASC LIMIT ?",
            (game_id, limit)
        )
        events = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return events
    
    def add_npc(self, game_id, name, description, relationship="neutral", first_met_round=1):
        """Add a new NPC to the game."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO npcs (game_id, name, description, relationship, first_met_round) VALUES (?, ?, ?, ?, ?)",
            (game_id, name, description, relationship, first_met_round)
        )
        
        conn.commit()
        conn.close()
    
    def update_npc(self, npc_id, description=None, relationship=None):
        """Update an NPC's information."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if relationship is not None:
            updates.append("relationship = ?")
            params.append(relationship)
        
        if updates:
            query = f"UPDATE npcs SET {', '.join(updates)} WHERE id = ?"
            params.append(npc_id)
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def get_npcs(self, game_id):
        """Get all NPCs for a game."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM npcs WHERE game_id = ?", (game_id,))
        npcs = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return npcs
    
    def update_inventory(self, game_id, items):
        """Update the player's inventory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE inventory SET items = ? WHERE game_id = ?",
            (json.dumps(items), game_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_inventory(self, game_id):
        """Get the player's inventory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT items FROM inventory WHERE game_id = ?", (game_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result['items'])
        return [] 