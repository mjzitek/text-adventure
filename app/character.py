"""
Character management module for the text adventure game.
"""
import os
from pathlib import Path
import random
class CharacterManager:
    """Manages character creation and information."""
    
    def __init__(self, db, llm_client):
        """Initialize the character manager."""
        self.db = db
        self.llm_client = llm_client

        self.genders = [
            "Male",
            "Female",
            "Non-Binary",
            "Agender",
            "Bigender",
            "Genderfluid",
            "Genderqueer",
            "Demiboy",
            "Demigirl",
            "Androgynous",
            "Two-Spirit",
            "Neutrois",
            "Polygender",
            "Third Gender",
            "Xenogender",
            "Questioning",

        ]

        self.backgrounds = [
            "Elementary School Teacher",
            "Movie Star",
            "Construction Worker",
            "Cardiologist",
            "Hedge Fund Specialist",
            "Career Politician",
            "Theoretical Physicist",
            "Stay-at-home Mom",
            "Mid-level Software Engineer",
            "Beet Farmer",
            "Manager of a struggling paper company",
            "High School Librarian",
            "Escape Room Designer",
            "Used Car Salesperson"
        ]

        self.traits_positive = [
            "Resourceful",
            "Brave",
            "Charismatic",
            "Strategic",
            "Cunning",
            "Resilient",
            "Empathetic",
            "Optimistic",
            "Tinkerer",
            "Sharp-Eyed"
        ]

        self.traits_neutral = [
            "Lone Wolf",
            "Sarcastic",
            "Risk-Taker",
            "Suspicious",
            "Pragmatic",
            "Obsessive",
            "Daydreamer",
            "Stubborn",
            "Rule-Breaker"
        ]

        self.traits_negative = [
            "Hot-Tempered",
            "Reckless",
            "Gullible",
            "Forgetful",
            "Anxious",
            "Greedy",
            "Self-Destructive",
            "Cowardly",
            "Arrogant",
        ]
    
    def create_character(self):
        """Create a new character through user interaction."""
        print("\n=== CHARACTER CREATION ===\n")
        print("Let's create your character for this post-apocalyptic adventure.\n")
        
        # Get character name
        name = ""
        while not name:
            name = input("What is your character's name? ").strip()
            if not name:
                print("You must enter a name.")
        
        # Select gender
        print("\nSelect your character's gender:")
        for i, gender in enumerate(self.genders, 1):
            print(f"{i}. {gender.title()}")
        print("0. Random")
        
        gender_choice = -1
        while gender_choice < 0 or gender_choice > len(self.genders):
            try:
                gender_choice = int(input(f"\nEnter a number (0-{len(self.genders)}): "))
            except ValueError:
                print("Please enter a valid number.")
        
        if gender_choice == 0:
            # Randomly select a gender
            gender = random.choice(self.genders)
        else:
            gender = self.genders[gender_choice - 1]

        # Select background
        print("\nSelect your character's background:")
        for i, bg in enumerate(self.backgrounds, 1):
            print(f"{i}. {bg.title()}")
        print("0. Random")
        
        background_choice = -1
        while background_choice < 0 or background_choice > len(self.backgrounds):
            try:
                background_choice = int(input(f"\nEnter a number (0-{len(self.backgrounds)}): "))
            except ValueError:
                print("Please enter a valid number.")
        
        if background_choice == 0:
            # Randomly select a background
            background = random.choice(self.backgrounds)
        else:
            background = self.backgrounds[background_choice - 1]
        
        # Select traits
        print("\nSelect your character's primary personality traits.")

        print("Positive Traits:")
        for i, trait in enumerate(self.traits_positive, 1):
            print(f"{i}. {trait.title()}")
        print("0. Random")
        
        positive_trait_choice = -1
        while positive_trait_choice < 0 or positive_trait_choice > len(self.traits_positive):
            try:
                positive_trait_choice = int(input(f"\nEnter a number (0-{len(self.traits_positive)}): "))
            except ValueError:
                print("Please enter a valid number.")
        
        if positive_trait_choice == 0:
            # Randomly select a positive trait
            positive_trait = random.choice(self.traits_positive)
        else:
            positive_trait = self.traits_positive[positive_trait_choice - 1]

        print("Neutral Traits:")
        for i, trait in enumerate(self.traits_neutral, 1):
            print(f"{i}. {trait.title()}")
        print("0. Random")
        
        neutral_trait_choice = -1
        while neutral_trait_choice < 0 or neutral_trait_choice > len(self.traits_neutral):
            try:
                neutral_trait_choice = int(input(f"\nEnter a number (0-{len(self.traits_neutral)}): "))
            except ValueError:
                print("Please enter a valid number.")
        
        if neutral_trait_choice == 0:
            # Randomly select a neutral trait
            neutral_trait = random.choice(self.traits_neutral)
        else:
            neutral_trait = self.traits_neutral[neutral_trait_choice - 1]

        print("Negative Traits:")
        for i, trait in enumerate(self.traits_negative, 1):
            print(f"{i}. {trait.title()}")
        print("0. Random")
        
        negative_trait_choice = -1
        while negative_trait_choice < 0 or negative_trait_choice > len(self.traits_negative):
            try:
                negative_trait_choice = int(input(f"\nEnter a number (0-{len(self.traits_negative)}): "))
            except ValueError:
                print("Please enter a valid number.")
        
        if negative_trait_choice == 0:
            # Randomly select a negative trait
            negative_trait = random.choice(self.traits_negative)
        else:
            negative_trait = self.traits_negative[negative_trait_choice - 1]
        
        traits = f"{positive_trait}, {neutral_trait}, {negative_trait}"

        print(f"\nYour character's traits are: {traits.title()}")

        # Generate character description
        print("\nGenerating your character description...")
        
        # Get template path
        template_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data" / "prompts" / "character_creation.txt"
        
        description = self.llm_client.generate_character_description(
            name, 
            gender,
            background, 
            traits,
            template_path if template_path.exists() else None
        )
        
        # Create character in database
        player = self.db.create_player(name, background, traits, description)
        
        # Display character info
        print("\n=== YOUR CHARACTER ===\n")
        print(f"Name: {name}")
        print(f"Gender: {gender}")
        print(f"Background: {background.title()}")
        print(f"Traits: {traits.title()}")
        print("\nDescription:")
        print(description)
        print("\nPress Enter to begin your adventure...")
        input()
        
        return player
    
    def get_character_summary(self, player):
        """Get a summary of the character."""
        return {
            "name": player["name"],
            "background": player["background"],
            "traits": player["traits"],
            "description": player["description"]
        } 