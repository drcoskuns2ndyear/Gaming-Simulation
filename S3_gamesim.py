
#stage3
from abc import ABC, abstractmethod
from collections import deque
import os

# =============================================================================
# UTIL
# =============================================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# =============================================================================
# BASE OBJECT
# =============================================================================

class GameObject(ABC):
    def __init__(self, name, position):
        self.name = name
        self.position = position

    @abstractmethod
    def move(self, game_map):
        pass

    @abstractmethod
    def attack(self, target):
        pass

# =============================================================================
# STRATEGY PATTERNS
# =============================================================================

class MovementStrategy(ABC):
    @abstractmethod
    def move(self, character, game_map):
        pass


class RandomMovement(MovementStrategy):
    def move(self, character, game_map):
        for dx, dy in DIRECTIONS:
            nx = character.position[0] + dx
            ny = character.position[1] + dy
            if game_map.is_inside((nx, ny)):
                character.position = (nx, ny)
                return


class ChasePlayerMovement(MovementStrategy):
    def move(self, character, game_map):
        path = game_map.bfs(character.position, game_map.player.position)
        if len(path) > 1:
            character.position = path[1]


class AttackStrategy(ABC):
    @abstractmethod
    def execute(self, attacker, target):
        pass


class MeleeAttack(AttackStrategy):
    def execute(self, attacker, target):
        dmg = attacker.weapon.damage if attacker.weapon else 5
        target.health -= dmg
        print(f"{attacker.name} hits {target.name} for {dmg} damage")

# =============================================================================
# COMPOSITION
# =============================================================================

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class Inventory:
    def __init__(self):
        self.items = []

# =============================================================================
# CHARACTER (ENCAPSULATION)
# =============================================================================

class Character(GameObject):
    def __init__(self, name, health, position):
        super().__init__(name, position)
        self._health = health
        self.alive = True
        self.weapon = None
        self.score = 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, value)
        if self._health == 0:
            self.alive = False

# =============================================================================
# PLAYER (INPUT CONTROLLED)
# =============================================================================

class Player(Character):
    def __init__(self, name, position):
        super().__init__(name, 100, position)
        self.inventory = Inventory()
        self.attack_strategy = MeleeAttack()

    def move(self, game_map):
        key = input("Move (W/A/S/D): ").lower()
        moves = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }
        if key in moves:
            dx, dy = moves[key]
            nx = self.position[0] + dx
            ny = self.position[1] + dy
            if game_map.is_inside((nx, ny)):
                self.position = (nx, ny)

    def attack(self, target):
        self.attack_strategy.execute(self, target)
        if not target.alive:
            self.score += 10

# =============================================================================
# ENEMY (AI)
# =============================================================================

class Enemy(Character):
    def __init__(self, name, health, position, movement_strategy):
        super().__init__(name, health, position)
        self.movement_strategy = movement_strategy
        self.attack_strategy = MeleeAttack()

    def move(self, game_map):
        self.movement_strategy.move(self, game_map)

    def attack(self, target):
        self.attack_strategy.execute(self, target)

# =============================================================================
# FACTORY PATTERN
# =============================================================================

class EnemyFactory:
    @staticmethod
    def create(enemy_type, position):
        if enemy_type == "goblin":
            e = Enemy("Goblin", 30, position, RandomMovement())
            e.weapon = Weapon("Dagger", 8)
            return e
        if enemy_type == "orc":
            e = Enemy("Orc", 60, position, ChasePlayerMovement())
            e.weapon = Weapon("Axe", 12)
            return e
        raise ValueError("Unknown enemy type")

# =============================================================================
# MAP + BFS PATHFINDING
# =============================================================================

DIRECTIONS = [(1,0), (-1,0), (0,1), (0,-1)]

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = None
        self.enemies = []

    def is_inside(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def bfs(self, start, goal):
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            if path[-1] == goal:
                return path

            x, y = path[-1]
            for dx, dy in DIRECTIONS:
                nxt = (x + dx, y + dy)
                if self.is_inside(nxt) and nxt not in visited:
                    visited.add(nxt)
                    queue.append(path + [nxt])
        return [start]

    def render(self):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        # önce düşmanlar çizilir
        for e in self.enemies:
            if e.alive:
                x, y = e.position
                grid[y][x] = "G" if e.name == "Goblin" else "O"

        # player HER ZAMAN en son çizilir (öncelik)
        px, py = self.player.position
        grid[py][px] = "P"

        print("\nMAP:")
        for row in grid:
            print(" ".join(row))

# =============================================================================
# GAME ENGINE
# =============================================================================

class GameEngine:
    def __init__(self, game_map, player, enemies):
        self.map = game_map
        self.player = player
        self.enemies = enemies
        self.turn = 0

        self.map.player = player
        self.map.enemies = enemies

    def run(self):
        while self.player.alive and self.enemies:
            self.step()

        clear()
        print("GAME OVER")
        print(f"Final Score: {self.player.score}")

    def step(self):
        self.turn += 1
        clear()
        print(f"TURN {self.turn}")
        print(f"HP: {self.player.health} | Score: {self.player.score}")

        self.map.render()
        self.player.move(self.map)

        for e in self.enemies:
            if e.alive:
                e.move(self.map)

        self.resolve_combat()

        self.enemies = [e for e in self.enemies if e.alive]
        self.map.enemies = self.enemies

    def resolve_combat(self):
        for e in self.enemies:
            if e.position == self.player.position:
                self.player.attack(e)
                if e.alive:
                    e.attack(self.player)

# =============================================================================
# MAIN
# =============================================================================

def main():
    game_map = GameMap(8, 6)

    player = Player("Hero", (0, 3))
    player.weapon = Weapon("Sword", 10)

    enemies = [
        EnemyFactory.create("goblin", (4, 2)),
        EnemyFactory.create("orc", (7, 3)),
        EnemyFactory.create("goblin", (5, 5)),
    ]

    engine = GameEngine(game_map, player, enemies)
    engine.run()

if __name__ == "__main__":
    main()
