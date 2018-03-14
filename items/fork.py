import libtcodpy as tcod


class Fork:
    def __init__(self):
        self.char = '%'
        self.color = tcod.blue

    def draw_info(self):
        return self.color, self.char
