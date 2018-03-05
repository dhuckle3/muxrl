import libtcodpy as tcod
from dungeon import Dungeon
from dungeon_view import DungeonView


class Main:
    def __init__(self):
        dungeon = Dungeon(11, 11)
        view = DungeonView(5, 5, 7, 7, dungeon)
        self.views = [view]
        self.viewport_width = 80
        self.viewport_height = 50
        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.viewport_width, self.viewport_height, 'muxRL', False)
        self.console = tcod.console_new(self.viewport_width, self.viewport_height)

    def handle_keys(self, key):
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_ESCAPE:
            return True
        player = self.views[0].dungeon.player
        if tcod.console_is_key_pressed(tcod.KEY_UP):
            player.move(0, -1)
        elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
            player.move(0, 1)
        elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
            player.move(-1, 0)
        elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
            player.move(1, 0)

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
        view_count = len(self.views)
        if view_count is 1:
            self.views[0].draw(self.console)


if __name__ == "__main__":
    main = Main()
    main.run()
