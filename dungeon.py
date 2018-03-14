import math
import libtcodpy as tcod
from tile import Tile
from character import Character
from dungeon_generator import DungeonGenerator

class Dungeon:
    def __init__(self, width, height, extra_enemies):
        self.rooms = []
        self.map = DungeonGenerator().generate_dungeon()

    def enemy_dict(self):
        character_dict = {}
        for x in range(self.width()):
            for y in range(self.height()):
                character = self.map[x][y].character
                if character is not None and not character.is_player():
                    character_dict[character] = [x, y]
        return character_dict

    def get_player(self):
        for x in range(self.width()):
            for y in range(self.height()):
                if self.map[x][y].has_player():
                    return self.map[x][y].character

    def is_player_alive(self):
        for x in range(self.width()):
            for y in range(self.height()):
                if self.map[x][y].has_player():
                    return True
        return False

    def get_display_center(self):
        for x in range(self.width()):
            for y in range(self.height()):
                if self.map[x][y].has_player():
                    return [x, y]

    def get_draw_info(self, x, y):
        tile = self.map[x][y]
        return tile.draw_info()

    def width(self):
        return len(self.map)

    def height(self):
        return len(self.map[0])

    def in_bounds(self, x, y):
        if x < 0 or y < 0:
            return False
        if x >= self.width() or y >= self.height():
            return False
        return True

    def move_character(self, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        old_tile = self.map[x][y]
        new_tile = self.map[new_x][new_y]
        if not new_tile.is_blocked() and not new_tile.is_occupied():
            new_tile.character = old_tile.character
            old_tile.character = None
        elif new_tile.is_occupied() and (old_tile.character.is_player() or new_tile.character.is_player()):
                new_tile.character = old_tile.character
                old_tile.character = None

    def distance_to(self, c1, c2):
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_enemies(self):
        enemies = self.enemy_dict()
        for c, v in enemies.items():
            if not c.is_player():
                if self.is_player_alive():
                    [player_x, player_y] = self.get_display_center()
                    if self.distance_to(v, [player_x, player_y]) > 6:
                        dx = tcod.random_get_int(0, -1, 1)
                        dy = tcod.random_get_int(0, -1, 1)
                        self.move_character(v[0], v[1], dx, dy)
                    else:
                        dx = sorted((-1, player_x - v[0], 1))[1]
                        dy = sorted((-1, player_y - v[1], 1))[1]
                        self.move_character(v[0], v[1], dx, dy)

    def advance_level(self):
        [x, y] = self.get_display_center()
        return self.map[x][y].char == '>'

    def check_fork(self):
        [x, y] = self.get_display_center()
        tile = self.map[x][y]
        if tile.item is not None:
            tile.item = None
            return True
        return False
