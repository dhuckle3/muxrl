import libtcodpy as tcod

from character import Character


class Main:
    def __init__(self):
        self.width = 80
        self.height = 50
        self.playerx = self.width // 2
        self.playery = self.height // 2
        window_title = 'muxRL'
        full_screen = False
        font_path = 'arial10x10.png'
        font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
        tcod.console_set_custom_font(font_path, font_flags)
        tcod.console_init_root(self.width, self.height, window_title, full_screen)
        self.console = tcod.console_new(self.width, self.height)
        tcod.console_set_default_foreground(self.console, tcod.white)
        self.characters = {}

    def setup_dungeon(self):
        player = Character(self.width // 2, self.height // 2, '@', tcod.white)
        npc = Character(self.width // 2 - 5, self.height // 2, '@', tcod.yellow)
        self.characters = {
            'player': player,
            'npc': npc
        }

    def handle_keys(self, key):
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_ESCAPE:
            return True

        print(self.characters)
        player = self.characters['player']
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
            for character in list(self.characters.values()):
                character.draw(self.console)
            tcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
            tcod.console_flush()
            key = tcod.console_wait_for_keypress(True)
            for character in list(self.characters.values()):
                character.clear(self.console)
            exit_requested = self.handle_keys(key)
            if exit_requested:
                break


if __name__ == "__main__":
    main = Main()
    main.setup_dungeon()
    main.run()
