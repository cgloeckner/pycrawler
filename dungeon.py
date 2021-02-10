#!/usr/bin/python3 
# -*- coding: utf-8 -*-


class Cell(object):
    def __init__(self, x, y, symbol):
        self.pos    = (x, y)
        self.symbol = symbol

    @staticmethod
    def Void(**kwargs):
        kwargs['symbol'] = '.'
        return Cell(**kwargs)
    
    @staticmethod
    def Wall(**kwargs):
        kwargs['symbol'] = '#'
        return Cell(**kwargs)

    @staticmethod
    def Floor(**kwargs):
        kwargs['symbol'] = ' '
        return Cell(**kwargs)

    def isVoid(self):
        return self.symbol == '.'

    def isWall(self):
        return self.symbol == '#'

    def isFloor(self):
        return self.symbol == ' '

    def getTexCoords(self):
        """ This assumes floors on row 1 and walls on row 2, where
        void has no texture. Also no texture variations are expected.
        """
        if self.isVoid():
            return None
        if self.isFloor():
            y = 0.0
        if self.isWall():
            y = 0.5
        # generate texture coordinates
        return (
            (0.0, y),       # top left
            (1.0, y),       # top right
            (1.0, y + 0.5), # bottom right
            (0.0, y + 0.5)  # bottom left
        )

# --------------------------------------------------------------------- 

class Dungeon(object):
    def __init__(self):
        self.size  = (0, 0)
        self.cells = list()

    def resize(self, w, h):
        self.size = w, h
        # rebuild all cells
        self.cells = [Cell.Void(x=None, y=None)] * w * h

    def has(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def mapIndex(self, x, y):
        if not self.has(x, y):
            raise KeyError('Invalid position <{0}|{1}>'.format(x, y))
        # map 2d coord to 1d index using dungeon's size
        return y * self.size[0] + x

    def get(self, x, y):
        return self.cells[self.mapIndex(x, y)]

    def set(self, x, y, cell):
        self.cells[self.mapIndex(x, y)] = cell

    def loadFromFile(self, fname):
        with open(fname, 'r') as h:
            content = h.read()
        lines = content.split('\n')

        # prepare cells array
        w = int(lines[0].split('x')[0])
        h = int(lines[0].split('x')[1])
        d = Dungeon()
        d.resize(w, h)
        
        # load from ascii
        y = 0
        for line in lines[1:]:
            x = 0
            for symbol in line:
                d.set(x, y, Cell(x, y, symbol))
                x += 1
            y += 1

        self.size  = d.size
        self.cells = d.cells

        return True

    def saveToFile(self, fname):
        # dump to ascii
        raw = '{0}x{1}'.format(*self.size)
        for i, cell in enumerate(self.cells):
            if i % self.size[0] == 0:
                raw += '\n'
            raw += cell.symbol
        
        with open(fname, 'w') as h:
            h.write(raw)

