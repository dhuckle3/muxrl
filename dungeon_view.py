import libtcodpy as tcod


class DungeonView:
    def __init__(self, x_start, y_start, width, height, dungeon):
        self.x_start = x_start
        self.y_start = y_start
        self.view_width = width
        self.view_height = height
        self.dungeon = dungeon

    def draw(self, console):
        [x_center, y_center] = self.dungeon.get_display_center()
        for x in range(self.view_width):
            for y in range(self.view_height):
                dungeon_x = x_center - (self.view_width // 2) + x
                dungeon_y = y_center - (self.view_height // 2) + y
                if self.dungeon.in_bounds(dungeon_x, dungeon_y):
                    [color, char] = self.dungeon.get_draw_info(dungeon_x, dungeon_y)
                    self.draw_char(console, char, color, self.x_start + x, self.y_start + y)
                else:
                    self.draw_char(console, ' ', tcod.light_blue, self.x_start + x, self.y_start + y)

    def clear(self, console):
        # todo remove if not needed?
        for x in range(self.x_start, self.x_start + self.view_width):
            for y in range(self.y_start, self.y_start + self.view_height):
                self.draw_char(console, ' ', tcod.black, x, y)

    @staticmethod
    def draw_char(console, char, color, x, y):
        tcod.console_set_default_foreground(console, color)
        tcod.console_put_char(console, x, y, char, tcod.BKGND_NONE)