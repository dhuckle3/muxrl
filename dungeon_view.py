import libtcodpy as tcod


class DungeonView:
    def __init__(self, x_start, y_start, width, height, dungeon, num):
        self.x_start = x_start
        self.y_start = y_start
        self.view_width = width
        self.view_height = height
        self.dungeon = dungeon
        self.number = num
        self.selected = False

    def set_selected(self, selected):
        self.selected = selected

    def border_color(self):
        if self.selected:
            return tcod.dark_green
        return tcod.light_grey

    def draw_border(self, console):
        for x in range(self.view_width):
            self.draw_background(console, x + self.x_start, self.y_start, self.border_color())
            self.draw_background(console, x + self.x_start, self.y_start + self.view_height - 1, self.border_color())
        for y in range(1, self.view_height):
            self.draw_background(console, self.x_start, y + self.y_start, self.border_color())
            self.draw_background(console, self.x_start + self.view_width - 1, y + self.y_start, self.border_color())
        numx = self.x_start + self.view_width//2
        numy = self.y_start + self.view_height - 1
        # tcod.console_put_char_ex(console, numx, numy, str(self.number), tcod.white, tcod.black)
        self.draw_background(console, self.x_start + self.view_width // 2, self.y_start + self.view_height - 1, tcod.black)
        self.draw_char(console, str(self.number), tcod.white, self.x_start + self.view_width // 2, self.y_start + self.view_height - 1)

    def draw(self, console):
        self.draw_border(console)
        [x_center, y_center] = self.dungeon.get_display_center()
        for x in range(1, self.view_width - 1):
            for y in range(1, self.view_height -1):
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
    def draw_background(console, x, y, color):
        tcod.console_set_char_background(console, x, y, color)

    @staticmethod
    def draw_char(console, char, color, x, y):
        tcod.console_set_default_foreground(console, color)
        tcod.console_put_char(console, x, y, char, tcod.BKGND_NONE)