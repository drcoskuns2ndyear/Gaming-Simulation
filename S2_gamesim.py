from abc import ABC, abstractmethod

# TEMEL CLASS ===========================================================================

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
      
# KOMPOZİSYON CLASSLARI =================================================================

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
class Inventory:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
      
# ORTAK CHARACTER CLASS ==================================================================
# (Encapsulation)

class Character(GameObject):
    def __init__(self, name, health, position=(0, 0)):
        super().__init__(name, position)
        self._health = health
        self.alive = True
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value):
        self._health = max(0, value)
        if self._health == 0:
            self.alive = False

# PLAYER CLASS ===========================================================================

class Player(Character):
    def __init__(self, name, health=100, position=(0, 0)):
        super().__init__(name, health, position)
        self.inventory = Inventory()
        self.weapon = None
    def move(self, direction):
        x, y = self.position
        moves = {
            "up": (x, y - 1),
            "down": (x, y + 1),
            "left": (x - 1, y),
            "right": (x + 1, y)
        }
        if direction in moves:
            self.position = moves[direction]
    def attack(self, target):
        damage = self.weapon.damage if self.weapon else 5
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage.")

# ENEMY CLASS ===========================================================================

class Enemy(Character):
    def __init__(self, name, health=50, position=(0, 0), weapon=None):
        super().__init__(name, health, position)
        self.weapon = weapon
    @classmethod
    def from_preset(cls, preset_name):
        presets = {
            "goblin": {"health": 30, "weapon": Weapon("Dagger", 8)},
            "orc": {"health": 60, "weapon": Weapon("Axe", 12)}
        }
        data = presets.get(preset_name, {"health": 20, "weapon": None})
        return cls(
            preset_name.capitalize(),
            data["health"],
            (0, 0),
            data["weapon"]
        )
    def move(self, direction):
        x, y = self.position
        if direction == "forward":
            self.position = (x + 1, y)
    def attack(self, target):
        damage = self.weapon.damage if self.weapon else 4
        target.health -= damage
        print(f"{self.name} hits {target.name} for {damage} damage.")

# ITEM CLASS ===========================================================================

class Item(GameObject):
    def __init__(self, name, effect, position=(0, 0)):
        super().__init__(name, position)
        self.effect = effect
    def move(self, direction):
        pass
    def attack(self, target):
        pass

# MAP & COLLISION ======================================================================

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def is_inside(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height
    def collision(self, objects):
        positions = {}
        collisions = []
        for obj in objects:
            if obj.position in positions:
                collisions.append((obj, positions[obj.position]))
            else:
                positions[obj.position] = obj
        return collisions

# GAME ENGINE (TURN-BASED) ==============================================================

class GameEngine:
    def __init__(self, game_map, players, enemies, items):
        self.map = game_map
        self.players = players
        self.enemies = enemies
        self.items = items
        self.turn = 0
    def step(self):
        self.turn += 1
        print(f"\n--- TURN {self.turn} ---")
       
        for player in self.players:
            player.move("right")
       
        for enemy in self.enemies:
            enemy.move("forward")
        
        collisions = self.map.collision(self.players + self.enemies)
        for obj1, obj2 in collisions:
            self.resolve_collision(obj1, obj2)

      
        self.enemies = [e for e in self.enemies if e.alive]
    def resolve_collision(self, obj1, obj2):
        if isinstance(obj1, Player) and isinstance(obj2, Enemy):
            obj1.attack(obj2)
            if obj2.alive:
                obj2.attack(obj1)
        elif isinstance(obj1, Enemy) and isinstance(obj2, Player):
            obj2.attack(obj1)
            if obj1.alive:
                obj1.attack(obj2)

# DEMO (STAGE 2 GÖSTERİMİ) ==============================================================

def main():
    game_map = GameMap(5, 5)
    player = Player("Hero", position=(0, 0))
    player.weapon = Weapon("Sword", 10)
    enemy = Enemy.from_preset("goblin")
    enemy.position = (1, 0)
    engine = GameEngine(
        game_map=game_map,
        players=[player],
        enemies=[enemy],
        items=[]
    )
    for _ in range(5):
        if not player.alive:
            print("Player died. Game Over.")
            break
        engine.step()
    print("\nGame finished.")
if __name__ == "__main__":
    main()
