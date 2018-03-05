import libtcodpy as tcod


class Tile:
    def __init__(self, x, y, char, blocked, block_sight, color):
        self.x = x
        self.y = y
        self.char = char
        self.blocked = blocked
        self.block_sight = block_sight
        self.color = color
        self.character = None

    def is_blocked(self):
        return self.blocked

    def is_occupied(self):
        return self.character is not None

    def draw(self, console):
        tcod.console_set_default_foreground(console, self.color)
        tcod.console_put_char(console, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, console):
        tcod.console_put_char(console, self.x, self.y, ' ', tcod.BKGND_NONE)

    def add_character(self, character):
        if self.is_occupied():
            return False
        self.character = character
