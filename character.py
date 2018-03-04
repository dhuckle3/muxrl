import libtcodpy as tcod


class Character:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        print('player position', self.x, self.y)

    def draw(self, console):
        tcod.console_set_default_foreground(console, self.color)
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        tcod.console_put_char(console, self.x, self.y, ' ', tcod.BKGND_NONE)
