class Tile:
    def __init__(self, x, y, char, blocked, block_sight, color):
        self.char = char
        self.blocked = blocked
        self.block_sight = block_sight
        self.color = color
        self.character = None

    def is_blocked(self):
        return self.blocked

    def draw_info(self):
        if self.is_occupied():
            return self.character.draw_info()
        return self.color, self.char

    def is_occupied(self):
        return self.character is not None

    def add_character(self, character):
        if self.is_occupied():
            return False
        self.character = character
