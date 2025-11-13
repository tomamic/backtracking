#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
"""

def download(url, name):
    try:
        from pyodide.http import open_url  # in the playground
        open(name, "w").write(open_url(url).read())
    except:
        from urllib.request import urlopen  # locally
        open(name, "wb").write(urlopen(url).read())

from os.path import isfile
if not isfile("g2d.py"):
    base = "https://raw.githubusercontent.com/fondinfo/fondinfo/master/"
    download(base + "g2d.py", "g2d.py")
    download(base + "g2d_pyodide.py", "g2d_pyodide.py")
    download(base + "boardgame.py", "boardgame.py")
    download(base + "boardgamegui.py", "boardgamegui.py")


from boardgame import BoardGame
from boardgamegui import gui_play

symbol = ["", "x", "o"]  # 0, 1, -1

class Connect4(BoardGame):
    def __init__(self, w: int, h: int):
        self._w, self._h = w, h
        self._board = [0] * (w * h)
        self._move = None
        self._turn = 1  # 1: MAX plr; -1: MIN plr
        self._winner = 0

    def _get(self, x, y):
        if 0 <= y < self._h and 0 <= x < self._w:
            return self._board[y * self._w + x]  # otherwise, None

    def _walk(self, x, y, dx, dy, v) -> int:
        if self._get(x, y) != v:
            return 0
        return 1 + self._walk(x + dx, y + dy, dx, dy, v)

    def _around(self, x, y, v) -> int:
        """Max line length of `v`s around and w/o `(x, y)`"""
        return max(self._walk(x + dx, y + dy, dx, dy, v) +
                   self._walk(x - dx, y - dy, -dx, -dy, v)
                   for dx, dy in [(0, -1), (1, -1), (1, 0), (1, 1)])

    def cols(self) -> int:
        return self._w

    def rows(self) -> int:
        return self._h

    def status(self) -> str:
        if not self.finished():
            return symbol[self._turn] + " plays"
        return (symbol[self._winner] or "None") + " wins"

    def read(self, x: int, y: int) -> str:
        p = symbol[self._get(x, y)]
        return p + ("!" if self._move == (x, y) else "")

    def play(self, x: int, y: int, command=""):
        y = self._walk(x, 0, 0, 1, 0) - 1
        if y >= 0:
            self._board[y * self._w + x] = self._turn
            self._move = x, y
            if self._around(x, y, self._turn) >= 3:
                self._winner = self._turn
            self._turn *= -1

    def finished(self) -> bool:
        return self._winner or all(self._board)

if __name__ == "__main__":
    gui_play(Connect4(7, 6))
