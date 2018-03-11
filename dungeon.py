import math
import libtcodpy as tcod
from rect import Rect
from tile import Tile
from character import Character


class Dungeon:
    def __init__(self, width, height):
        self.rooms = []
        self.map = self.make_map(width, height)
        self.generate_dungeon()


    @staticmethod
    def make_map(width, height):
        return [[Tile(' ', True, tcod.grey) for y in range(height)] for x in range(width)]

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

    def create_entrance_room(self):
        self.create_room(0, 0, 7, 7)

    def create_room(self, x0, y0, width, height):
        for x in range(x0, x0 + width):
            for y in range(y0, y0 + height):
                self.map[x][y] = Tile('.', False, tcod.white)
        for x in range(x0, x0 + width):
            self.map[x][y0] = Tile('#', True, tcod.white)
            self.map[x][y0 + height - 1] = Tile('#', True, tcod.white)
        for y in range(y0, y0 + height):
            self.map[x0][y] = Tile('#', True, tcod.white)
            self.map[x0 + width - 1][y] = Tile('#', True, tcod.white)

    def create_rect(self):
        max_size = 10
        min_size = 6
        w = tcod.random_get_int(0, min_size, max_size)
        h = tcod.random_get_int(0, min_size, max_size)
        x = tcod.random_get_int(0, 0, self.width() - w - 1)
        y = tcod.random_get_int(0, 0, self.height() - h - 1)
        return Rect(x, y, w, h)

    def build_tunnel(self, room1, room2):
        [x1, y1] = room1.center()
        [x2, y2] = room2.center()
        if tcod.random_get_int(0, 0, 1) == 1:
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def intersect(self, rect):
        for x in range(rect.x1, rect.x2 + 1):
            for y in range(rect.y1, rect.y2 + 1):
                if self.map[x][y].char != ' ':
                    return True
        return False

    def generate_dungeon(self):
        max_rooms = 30
        for r in range(max_rooms):
            new_rect = self.create_rect()
            failed = False
            for room in self.rooms:
                if new_rect.intersect(room) and self.intersect(new_rect):
                    failed = True
                    break
            if not failed:
                room_count = len(self.rooms)
                self.rooms.append(new_rect)
                self.create_room(new_rect.x1, new_rect.y1, new_rect.x2 - new_rect.x1, new_rect.y2 - new_rect.y1)
                if room_count > 0:
                    self.build_tunnel(self.rooms[room_count-1], new_rect)
        [x, y] = self.rooms[0].center()
        self.map[x][y].add_character(Character(self, '@', tcod.white))
        self.add_enemies(10)

    def add_enemies(self, enemy_count):
        for i in range(enemy_count):
            room_num = tcod.random_get_int(0, 0, len(self.rooms))
            room = self.rooms[room_num-1]
            placed = False
            tries = 0
            while not placed and tries < 10:
                tries += 1
                x = tcod.random_get_int(0, room.x1 + 1, room.x2)
                y = tcod.random_get_int(0, room.y1 + 1, room.y2)
                tile = self.map[x][y]
                if not tile.is_occupied() and not tile.is_blocked():
                    tile.add_character(Character(self, 'g', tcod.dark_green))
                    placed = True

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

    def create_h_tunnel(self, x0, x1, y):
        print(x0, x1, y)
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.map[x][y] = Tile('-', False, tcod.light_amber)

    def create_v_tunnel(self, y0, y1, x):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.map[x][y] = Tile('|', False, tcod.light_amber)

    def distance_to(self, c1, c2):
        print(c1, c2)
        dx = c1[0] - c2[0]
        dy = c1[1] - c2[1]
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_enemies(self):
        characters = self.enemy_dict()
        for c, v in characters.items():
            if not c.is_player():
                [player_x, player_y] = self.get_display_center()
                if self.distance_to(v, [player_x, player_y]) > 6:
                    dx = tcod.random_get_int(0, -1, 1)
                    dy = tcod.random_get_int(0, -1, 1)
                    self.move_character(v[0], v[1], dx, dy)