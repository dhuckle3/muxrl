class Character:
    def __init__(self, dungeon_map, x, y, char, color):
        self.dungeon_map = dungeon_map
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        x, y = self.x + dx, self.y + dy
        tile = self.dungeon_map[x][y]
        if not tile.is_blocked() and not tile.is_occupied():
            self.dungeon_map[self.x][self.y].character = None
            self.x, self.y = [x, y]
            self.dungeon_map[self.x][self.y].character = self

    def draw_info(self):
        return self.color, self.char
