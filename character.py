class Character:
    def __init__(self, dungeon, char, color):
        self.dungeon = dungeon
        self.char = char
        self.color = color

    def move(self, dx, dy):
        self.dungeon.move_character(self, dx, dy)

    def draw_info(self):
        return self.color, self.char

    def is_player(self):
        return self.char == '@'
