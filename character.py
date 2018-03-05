import libtcodpy as tcod


class Character:
    def __init__(self, map, x, y, char, color):
        self.map = map
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        print('move')
        x, y = self.x + dx, self.y + dy
        tile = self.map[x][y]
        if not tile.is_blocked() and not tile.is_occupied():
            self.x, self.y = [x, y]
            print('New player position', self.x, self.y)

    def draw(self, console):
        tcod.console_set_default_foreground(console, self.color)
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        tcod.console_put_char(console, self.x, self.y, ' ', tcod.BKGND_NONE)
