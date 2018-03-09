import libtcodpy as tcod
from dungeon import Dungeon
from dungeon_view import DungeonView


class Main:
    def __init__(self):

        self.control_active = False
        self.views = []
        self.views.append(DungeonView(3, 3, 13, 13, Dungeon(11, 11), 1))
        self.views.append(DungeonView(15, 3, 13, 13, Dungeon(11, 11), 2))
        self.views.append(DungeonView(27, 3, 13, 13, Dungeon(11, 11), 3))
        self.views.append(DungeonView(39, 3, 13, 13, Dungeon(11, 11), 4))
        self.viewport_width = 80
        self.viewport_height = 50
        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.viewport_width, self.viewport_height, 'muxRL', False)
        self.console = tcod.console_new(self.viewport_width, self.viewport_height)
        self.select_all_views()

    def handle_keys(self, key):
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_ESCAPE:
            return True
        if key.vk == tcod.KEY_UP or tcod.console_is_key_pressed(tcod.KEY_KP8):
            self.move_north()
        elif key.vk == tcod.KEY_KP9:
            self.move_northeast()
        elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
            self.move_east()
        elif key.vk == tcod.KEY_KP3:
            self.move_southeast()
        elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
            self.move_south()
        elif key.vk == tcod.KEY_KP1:
            self.move_southwest()
        elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
            self.move_west()
        elif key.vk == tcod.KEY_KP7:
            self.move_northwest()
        elif key.vk == tcod.KEY_CONTROL and key.c == ord('a'):
            self.control_active = True
        elif key.c == ord('a'):
            self.select_all_views()
        elif key.c >= ord('1') and key.c <= ord('9'):
            self.control_active = False
            for view in self.views:
                view.set_selected(False)
            index = int(chr(key.c)) - 1
            if index in range(len(self.views)):
                print('selecting', index)
                self.select_dungeon_view(self.views[index])

    def select_all_views(self):
        self.selected_player = None
        for view in self.views:
            view.set_selected(True)

    def select_dungeon_view(self, view):
        self.selected_player = view.dungeon.player;
        view.set_selected(True)

    def move_player(self, x, y):
        if self.selected_player is None:
            for view in self.views:
                player = view.dungeon.player
                player.move(x, y)
        else:
            self.selected_player.move(x, y)

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
            tcod.console_blit(self.console, 0, 0, self.viewport_width, self.viewport_height, 0, 0, 0)
            tcod.console_flush()
            key = tcod.console_wait_for_keypress(True)
            self.clear()
            exit_requested = self.handle_keys(key)
            if exit_requested:
                break

    def clear(self):
        for view in self.views:
            view.clear(self.console)

    def draw(self):
        tcod.console_set_char_foreground(self.console, 1, 1, tcod.white)
        for view in self.views:
            if not view.selected:
                view.draw(self.console)
        for view in self.views:
            if view.selected:
                view.draw(self.console)


if __name__ == "__main__":
    main = Main()
    main.run()
