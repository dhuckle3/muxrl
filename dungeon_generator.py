import tcod
from tile import Tile
from items.fork import Fork
from character import Character
from items.fork import Fork
from rect import Rect


class DungeonGenerator:
    def __init__(self):
        self.width = 40
        self.height = 30
        self.max_rooms = 30
        self.rooms = []
        self.map = self.make_map(self.width, self.height)

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

    def create_entrance_room(self):
        self.create_room(0, 0, 7, 7)

    def create_room(self, x0, y0, width, height):
        for x in range(x0, x0 + width):
            for y in range(y0, y0 + height):
                self.map[x][y] = Tile('.', False, tcod.white)
        for x in range(x0, x0 + width):
            self.map[x][y0] = Tile('#', True, tcod.dark_gray)
            self.map[x][y0 + height - 1] = Tile('#', True, tcod.dark_gray)
        for y in range(y0, y0 + height):
            self.map[x0][y] = Tile('#', True, tcod.dark_gray)
            self.map[x0 + width - 1][y] = Tile('#', True, tcod.dark_gray)

    def create_rect(self):
        max_size = 10
        min_size = 6
        w = tcod.random_get_int(0, min_size, max_size)
        h = tcod.random_get_int(0, min_size, max_size)
        x = tcod.random_get_int(0, 0, self.width - w - 1)
        y = tcod.random_get_int(0, 0, self.height - h - 1)
        return Rect(x, y, w, h)

    def generate_dungeon(self):
        for r in range(self.max_rooms):
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
                    self.build_tunnel(self.rooms[room_count - 1], new_rect)
        [x, y] = self.rooms[0].center()
        self.add_exit()
        self.map[x][y] = Tile('<', False, tcod.yellow)
        self.map[x][y].add_character(Character(self, '@', tcod.white))
        self.add_fork()
        return self.map

    def add_fork(self):
        room_num = tcod.random_get_int(0, 0, len(self.rooms))
        room = self.rooms[room_num-1]
        placed = False
        tries = 0
        while not placed and tries < 10:
                tries += 1
                x = tcod.random_get_int(0, room.x1 + 2, room.x2 -1)
                y = tcod.random_get_int(0, room.y1 + 2, room.y2 -1)
                tile = self.map[x][y]
                if not tile.is_occupied() and not tile.is_blocked():
                    self.map[x][y].add_item(Fork())
                    placed = True

    def add_exit(self):
        room_num = tcod.random_get_int(0, 0, len(self.rooms))
        room = self.rooms[room_num-1]
        placed = False
        tries = 0
        while not placed and tries < 10:
                tries += 1
                x = tcod.random_get_int(0, room.x1 + 2, room.x2 -1)
                y = tcod.random_get_int(0, room.y1 + 2, room.y2 -1)
                tile =self.map[x][y]
                if not tile.is_occupied() and not tile.is_blocked():
                    self.map[x][y] = Tile('>', False, tcod.yellow)
                    placed = True

    def intersect(self, rect):
        for x in range(rect.x1, rect.x2 + 1):
            for y in range(rect.y1, rect.y2 + 1):
                if self.map[x][y].char != ' ':
                    return True
        return False

    def build_tunnel(self, room1, room2):
        [x1, y1] = room1.center()
        [x2, y2] = room2.center()
        if tcod.random_get_int(0, 0, 1) == 1:
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def create_h_tunnel(self, x0, x1, y):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.map[x][y] = Tile('-', False, tcod.white)

    def create_v_tunnel(self, y0, y1, x):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.map[x][y] = Tile('|', False, tcod.white)

    @staticmethod
    def make_map(width, height):
        return [[Tile(' ', True, tcod.grey) for y in range(height)] for x in range(width)]
