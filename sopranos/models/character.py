from typing import List, Optional
from ..utils.errors import CharacterNotFoundError

class Character:
    def __init__(self, id: int, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

# Sample characters data
characters = [
    Character(1, "Tony", "Soprano"),
    Character(2, "Carmela", "Soprano"),
    Character(3, "Christopher", "Moltisanti"),
    Character(4, "Silvio", "Dante"),
    Character(5, "Paulie", "Walnuts"),
    Character(6, "Salvatore", "Bonpensiero"),
    Character(7, "Adriana", "La Cerva"),
    Character(8, "Meadow", "Soprano"),
    Character(9, "Anthony", "Soprano Jr."),
    Character(10, "Livia", "Soprano")
]

def get_character_by_id(character_id: int) -> Optional[Character]:
    character = next((char for char in characters if char.id == character_id), None)
    if character is None:
        raise CharacterNotFoundError(character_id)
    return character

def search_characters(first_name: Optional[str] = None, last_name: Optional[str] = None) -> List[Character]:
    filtered_characters = characters
    
    if first_name:
        first_name = first_name.lower()
        filtered_characters = [
            char for char in filtered_characters
            if first_name in char.first_name.lower()
        ]
    
    if last_name:
        last_name = last_name.lower()
        filtered_characters = [
            char for char in filtered_characters
            if last_name in char.last_name.lower()
        ]
    
    return filtered_characters 