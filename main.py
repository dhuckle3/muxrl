import libtcodpy as tcod
from dungeon import Dungeon
from dungeon_view import DungeonView


class Main:
    def __init__(self):
        self.control_active = False
        self.views = []
        self.max_rows = 3
        self.viewport_width = 80
        self.viewport_height = 60
        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.viewport_width, self.viewport_height, 'muxRL', False)
        self.console = tcod.console_new(self.viewport_width, self.viewport_height)
        self.add_dungeon_view()
        self.update_views()
        self.select_all_views()

    def handle_keys(self, key):
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_ESCAPE:
            return True
        if key.vk == tcod.KEY_UP or tcod.console_is_key_pressed(tcod.KEY_KP8) or key.c == ord('k'):
            self.move_north()
        elif key.vk == tcod.KEY_KP9 or key.c == ord('u'):
            self.move_northeast()
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6 or key.c == ord('l'):
            self.move_east()
        elif key.vk == tcod.KEY_KP3 or key.c == ord('n'):
            self.move_southeast()
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2 or key.c == ord('j'):
            self.move_south()
        elif key.vk == tcod.KEY_KP1 or key.c == ord('b'):
            self.move_southwest()
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4 or key.c == ord('h'):
            self.move_west()
        elif key.vk == tcod.KEY_KP7 or key.c == ord('y'):
            self.move_northwest()
        elif key.c == ord('a') and self.control_active:
            self.select_all_views()
        elif tcod.console_is_key_pressed(tcod.KEY_CONTROL) and key.c == ord('a'):
            self.control_active = True
        elif key.c >= ord('1') and key.c <= ord('9') and self.control_active:
            self.control_active = False
            for view in self.views:
                view.set_selected(False)
            index = int(chr(key.c)) - 1
            if index in range(len(self.views)):
                self.views[index].set_selected(True)
        elif key.c == ord('d'):
            if len(self.views) < 9:
                self.add_dungeon_view()

    def update_views(self):
        view_count = len(self.views)
        width = self.viewport_width
        height = self.viewport_height
        rows = (view_count - 1) // self.max_rows + 1
        view_height = height // rows
        for row in range(rows):
            row_views = len(self.views) - (row * self.max_rows)
            if row_views > self.max_rows:
                row_views = self.max_rows
            view_width = width // row_views
            x_off = (width - view_width * row_views) // 2
            for column in range(row_views):
                index = row * self.max_rows + column
                x0 = x_off + view_width * column
                y0 = view_height * row
                x1 = x0 + view_width
                y1 = y0 + view_height
                self.views[index].set_position(x0, y0, x1, y1)

    def add_dungeon_view(self):
        view = DungeonView(self.console, Dungeon(40, 30))
        view.set_selected(True)
        self.views.append(view)
        self.update_views()

    def select_all_views(self):
        for view in self.views:
            view.set_selected(True)

    def select_dungeon_view(self, view):
        view.set_selected(True)

    def move_player(self, dx, dy):
        for view in self.views:
            if view.selected:
                [x, y] = view.dungeon.get_display_center()
                view.dungeon.move_character(x, y, dx, dy)

    def move_north(self):
        self.move_player(0, -1)

    def move_northeast(self):
        self.move_player(1, -1)

    def move_east(self):
        self.move_player(1, 0)

    def move_southeast(self):
        self.move_player(1, 1)

    def move_south(self):
        self.move_player(0, 1)

    def move_southwest(self):
        self.move_player(-1, 1)

    def move_west(self):
        self.move_player(-1, 0)

    def move_northwest(self):
        self.move_player(-1, -1)

    def run(self):
        while not tcod.console_is_window_closed():
            self.draw()
            key = tcod.console_wait_for_keypress(True)
            exit_requested = self.handle_keys(key)
            if exit_requested:
                break

    def draw(self):
        for c, view in enumerate(self.views):
            if not view.selected:
                view.draw(self.console, c + 1)
        for c, view in enumerate(self.views):
            if view.selected:
                view.draw(self.console, c + 1)
        tcod.console_blit(self.console, 0, 0, self.viewport_width, self.viewport_height, 0, 0, 0)
        tcod.console_flush()


if __name__ == "__main__":
    main = Main()
    main.run()
