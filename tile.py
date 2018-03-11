class Tile:
    def __init__(self, char, blocked, color):
        self.char = char
        self.blocked = blocked
        # self.block_sight = block_sight
        self.color = color
        self.character = None
        self.item = None

    def is_blocked(self):
        return self.blocked

    def is_occupied(self):
        return self.character is not None

    def draw_info(self):
        if self.is_occupied():
            return self.character.draw_info()
        elif self.item is not None:
            return self.item.draw_info()
        else:
            return self.color, self.char

    def add_character(self, character):
        if self.is_occupied():
            return False
        self.character = character

    def add_item(self, item):
        self.item = item

    def has_player(self):
        if self.is_occupied():
            return self.character.is_player()
        return False
