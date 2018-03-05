import libtcodpy as tcod
from tile import Tile
from character import Character


class Dungeon:
    def __init__(self, width, height):
        self.map = self.make_map(width, height)
        self.player = Character(self.map, width // 2, height // 2, '@', tcod.white)
        self.map[self.player.x][self.player.y].add_character(self.player)
        npc = Character(self.map, width // 2 - 2, height // 2, '@', tcod.yellow)
        self.map[npc.x][npc.y].add_character(npc)

    def get_display_center(self):
        return self.player.x, self.player.y

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

    @staticmethod
    def make_map(width, height):
        result = [[Tile(x, y, '.', False, False, tcod.grey) for y in range(width)] for x in range(width)]
        for x in range(width):
            result[x][0] = Tile(x, 0, '#', True, True, tcod.white)
            result[x][height - 1] = Tile(x, height-1, '#', True, True, tcod.white)
        for y in range(height):
            result[0][y] = Tile(0, y, '#', True, True, tcod.white)
            result[width - 1][y] = Tile(width - 1, y, '#', True, True, tcod.white)
        return result
