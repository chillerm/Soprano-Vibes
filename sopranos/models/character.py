class Character:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
    
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name
        }

# Sample characters data
characters = [
    Character("Tony", "Soprano"),
    Character("Carmela", "Soprano"),
    Character("Christopher", "Moltisanti"),
    Character("Silvio", "Dante"),
    Character("Paulie", "Walnuts"),
    Character("Salvatore", "Bonpensiero"),
    Character("Adriana", "La Cerva"),
    Character("Meadow", "Soprano"),
    Character("Anthony", "Soprano Jr."),
    Character("Livia", "Soprano")
] 