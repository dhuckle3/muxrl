import libtcodpy as tcod
from tile import Tile
from character import Character


class Dungeon:
    def __init__(self, width, height):
        self.map = self.make_map(width, height)
        self.generate_dungeon()

    @staticmethod
    def make_map(width, height):
        return [[Tile(' ', False, tcod.grey) for y in range(height)] for x in range(width)]

    def character_dict(self):
        character_dict = {}
        for x in range(self.width()):
            for y in range(self.height()):
                character = self.map[x][y].character
                character_dict[character] = [x, y]
        return character_dict

    def get_player(self):
        for x in range(self.width()):
            for y in range(self.height()):
                if self.map[x][y].has_player():
                    return self.map[x][y].character

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

    def create_entrance_room(self):
        self.create_room(0, 0, 7, 7)

    def create_room(self, x0, y0, width, height):
        for x in range(x0, width):
            for y in range(y0, height):
                self.map[x][y] = Tile('.', False, tcod.white)
        for x in range(x0, width):
            self.map[x][0] = Tile('#', True, tcod.white)
            self.map[x][height - 1] = Tile('#', True, tcod.white)
        for y in range(y0, height):
            self.map[0][y] = Tile('#', True, tcod.white)
            self.map[width - 1][y] = Tile('#', True, tcod.white)

    def generate_dungeon(self):
        self.create_entrance_room()
        self.map[2][2].add_character(Character(self, '@', tcod.white))

    def move_character(self, x, y, dx, dy):
        new_x, new_y = x + dx, y + dy
        old_tile = self.map[x][y]
        new_tile = self.map[new_x][new_y]
        if not new_tile.is_blocked() and not new_tile.is_occupied():
            new_tile.character = old_tile.character
            old_tile.character = None
