
import random


class Pokemon:
    def __init__(self, data=None):
        self.id = ""
        self.name = ""
        self.type = ""
        self.level = 0  
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.hp = random.randint(50, 101)  # Random HP between 50 and 150
        self.initilized = False
        if data:
            self.initilized = True
            self.id = int(data[0])
            self.name = data[1]
            self.type = data[2] 
            self.level = int(data[3])
            self.attack = int(data[4])
            self.defense = int(data[5])
            self.speed = int(data[6])
    def __str__(self):
        return f"Pokemon(ID: {self.id}, Name: {self.name}, Type: {self.type}, Level: {self.level}, Attack: {self.attack}, Defense: {self.defense}, Speed: {self.speed})"
    
    @property
    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "hp": self.hp
        }