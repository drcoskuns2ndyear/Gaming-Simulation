from abc import ABC, abstractmethod

#Temel Classlar------------------------------------------------------

class GameObject(ABC):
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.position = position

    @abstractmethod
    def move(self, direction):
        pass

    @abstractmethod
    def attack(self, target):
        pass

#Kompozisyon Classları-------------------------------------------------

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

#Oyuncu Classları------------------------------------------------------

class Player(GameObject):
    def __init__(self, name, health=100, position=(0, 0)):
        super().__init__(name, position)
        self.health = health
        self.inventory = Inventory()
        self.weapon = None

    def move(self, direction):
        x, y = self.position
        if direction == "up":
            self.position = (x, y - 1)
        elif direction == "down":
            self.position = (x, y + 1)
        elif direction == "left":
            self.position = (x - 1, y)
        elif direction == "right":
            self.position = (x + 1, y)

    def attack(self, target):
        if self.weapon is None:
            damage = 5  #Basit bir yumruk diyelim şimdilik
        else:
            damage = self.weapon.damage

        target.health -= damage
        print(f"{self.name} attacked {target.name} for {damage} damage.")

#Düşman Classları--------------------------------------------------------

class Enemy(GameObject):
    def __init__(self, name, health=50, position=(0, 0), weapon=None):
        super().__init__(name, position)
        self.health = health
        self.weapon = weapon

    @classmethod
    def from_preset(cls, preset_name):
        presets = {
            "goblin": {"health": 30, "weapon": Weapon("Dagger", 8)},
            "orc": {"health": 60, "weapon": Weapon("Axe", 12)}
        }
        data = presets.get(preset_name, {"health": 20, "weapon": None})
        return cls(preset_name.capitalize(), data["health"], (0, 0), data["weapon"])

    def move(self, direction):
        #Basit hareket olsun
        x, y = self.position
        if direction == "forward":
            self.position = (x + 1, y)

    def attack(self, target):
        damage = self.weapon.damage if self.weapon else 4
        target.health -= damage
        print(f"{self.name} hits {target.name} for {damage} damage.")

#İtem Classları---------------------------------------------------------

class Item(GameObject):
    def __init__(self, name, effect, position=(0, 0)):
        super().__init__(name, position)
        self.effect = effect 

    def move(self, direction):
        pass #İtemler hareket etmiyorlar :/

    def attack(self, target):
        pass  #İtemler atak yapmıyorlar :p
#The End...
