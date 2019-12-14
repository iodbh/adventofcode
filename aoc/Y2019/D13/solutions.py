from ...classes import Solution
from ..classes import IntCode
from time import sleep
import curses
import unicodedata

ARCADE_TILES = {
    # Empty Tile:
    0: {"str": "  ", "name": "empty"},
    # Wall:
    1: {"str": "  ", "colors": 2, "name": "wall"},
    # Block:
    2: {"str": "  ", "colors": 1, "name": "block"},
    # Horizontal Paddle:
    3: {"str": unicodedata.lookup("BOX DRAWINGS HEAVY HORIZONTAL")*2, "name": "paddle"},
    # Ball
    4: {"str": unicodedata.lookup("LEFT HALF BLACK CIRCLE") + unicodedata.lookup("RIGHT HALF BLACK CIRCLE"), "name": "ball", "colors": 3}
}


def chunk(iter, size):
    for i in range(0, len(iter), size):
        yield iter[i:i + size]


class ArcadeCabinet:
    def __init__(self, program, screen_width=50, screen_height=50, scr=None, display=False, autoplay=False):
        self.cpu = IntCode(program, silent=True, input_wait=True)
        self.screen_width = screen_width
        self.screen_height = screen_height + 1
        self.screen = Screen(self.screen_width, self.screen_height, scr=scr, virtual=not display)
        self.screen_state = [[0 for col in range(self.screen_width)] for line in range(screen_height)]
        self.display = display
        self.joystick = 0
        self.score = 0
        if scr is not None:
            curses.halfdelay(1)
        self.autoplay = autoplay

    def _get_joystick(self):
        j = self.joystick
        self.joystick = 0
        return j

    def run_game(self, loop=False, delay=0):
        mem, out = self.cpu.run_program()
        ball_x = -1
        ball_x_prev = -1
        paddle_x = -1
        while self.cpu.waiting:
            for x, y, tile in chunk(out, 3):
                if x == -1:
                    if self.display:
                        self.screen.scr.addstr(self.screen_height - 1, 0, str(tile))
                    self.score = tile
                else:
                    if tile == 4:
                        ball_x_prev = ball_x
                        ball_x = x
                    elif tile == 3:
                        paddle_x = x
                    if self.display:
                        self.screen.draw_tile(x, y, tile)
                    self.screen_state[y][x] = tile
            if self.autoplay:
                if ball_x < paddle_x:
                    # ball is to the left
                    if ball_x_prev < ball_x:
                        # ball is going to right
                        key = None
                    elif ball_x_prev > ball_x:
                        # ball is going right to left
                        key = curses.KEY_LEFT
                    else:
                        key = curses.KEY_LEFT
                elif ball_x > paddle_x:
                    # ball is to the right
                    if ball_x_prev < ball_x:
                        # ball is going to right
                        key = curses.KEY_RIGHT
                    elif ball_x_prev > ball_x:
                        # ball is going right to left
                        key = None
                    else:
                        key = curses.KEY_RIGHT
            else:
                key = self.screen.scr.getch()
            if key == curses.KEY_LEFT:
                self.joystick = -1
            elif key == curses.KEY_RIGHT:
                self.joystick += 1
            else:
                self.joystick += 0
            sleep(delay)
            mem, out = self.cpu.run_program(inputs=[self._get_joystick()])
        if out[-2] == -1:
            self.score = str(out[-1])
        if self.display and loop:
            while True:
                pass
        return self.score


class Screen:

    def __init__(self, width, height, scr=None, wrapped=False, tiles=ARCADE_TILES, virtual=False):
        self.width = width
        self.height = height
        self.scr = scr
        self.wrapped = wrapped
        self.tiles = tiles
        if not virtual:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    def draw_tile(self, x, y, tile):
        tilespec = self.tiles[tile]
        if "colors" in tilespec:
            self.scr.addstr(*self._coords(x, y), tilespec["str"], curses.color_pair(tilespec["colors"]))
        else:
            self.scr.addstr(*self._coords(x, y), tilespec["str"])
        self.scr.refresh()

    def _coords(self, x, y):
        """
        Returns the coordinates inverted to match curse's format, and x is
        doubled to match the 2-cols drawing system.
        """
        return y, x * 2

    def _setup_window(self):
        if self.width * 2 > curses.COLS or self.height > curses.LINES:
            raise ValueError(f"The screen size exceeds the terminal size. max height: {curses.COLS//2}. Max width: {curses.LINES}")
        self.win = curses.newwin(self.width, self.height)

    def setup(self):
        stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

    def shutdown(self):
        curses.nocbreak()
        if self.scr:
            self.scr.keypad(False)
        curses.echo()
        curses.endwin()


def display_loop(scr, data, display=False, autoplay=False, loop=False):
    cabinet = ArcadeCabinet(data, scr=scr, display=display, autoplay=autoplay)
    cabinet.run_game(loop=loop)
    return cabinet


def phase1(data):
    #curses.wrapper(display_loop, data)
    cabinet = display_loop(None, data)
    screen_state = cabinet.screen_state
    total = 0
    for line in screen_state:
        for cell in line:
            if cell == 2:
                total += 1
    return total


def phase2(data):
    data[0] = 2
    cabinet = display_loop(None, data, display=False, autoplay=True)
    return cabinet.score


solution = Solution(2019, 13, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
