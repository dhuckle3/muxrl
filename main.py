import libtcodpy as tcod

from character import Character
from tile import Tile


class Main:
    def __init__(self):
        self.width = 80
        self.height = 50
        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(self.width, self.height, 'muxRL', False)
        self.console = tcod.console_new(self.width, self.height)
        tcod.console_set_default_foreground(self.console, tcod.white)
        self.make_map()
        self.map = self.make_map()
        player = Character(self.map, self.width // 2, self.height // 2, '@', tcod.white)
        npc = Character(self.map, self.width // 2 - 5, self.height // 2, '@', tcod.yellow)
        self.map[npc.x][npc.y].add_character(npc)
        self.characters = {
            'player': player,
            'npc': npc
        }

    def make_map(self):
        result = [[Tile(x, y, '.', False, False, tcod.grey) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            result[x][0] = Tile(x, 0, '#', True, True, tcod.white)
            result[x][self.height-1] = Tile(x, self.height - 1, '#', True, True, tcod.white)
        for y in range(self.height):
            result[0][y] = Tile(0, y, '#', True, True, tcod.white)
            result[self.width-1][y] = Tile(self.width - 1, y, '#', True, True, tcod.white)
        return result

    def draw_tile(self, tile):
        tile.draw(self.console)

    def handle_keys(self, key):
        if key.vk == tcod.KEY_ENTER and key.lalt:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif key.vk == tcod.KEY_ESCAPE:
            return True
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
            self.draw()
            tcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 0, 0)
            tcod.console_flush()
            key = tcod.console_wait_for_keypress(True)
            self.clear()
            exit_requested = self.handle_keys(key)
            if exit_requested:
                break

    def clear(self):
        for character in list(self.characters.values()):
            character.clear(self.console)

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                self.draw_tile(self.map[x][y])
        for character in list(self.characters.values()):
            character.draw(self.console)


if __name__ == "__main__":
    main = Main()
    main.run()
