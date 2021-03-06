#!/usr/bin/python3 
# -*- coding: utf-8 -*-


class VertexBuilder(object):
    """ Builds dungeon tile vertices. (x, y) are relative to the flat
    2D dungeon layout where as z indiciates the height. These are NOT
    following the OpenGL coordinate system but allow for simpler
    navigation on a dungeon level.
    """
    
    def __init__(self):
        self.data = list()

    def no_walls(self):
        # monkeypatch to replace walls with empty vertices
        zero_quad  = tuple([(0.0, 0.0, 0.0)] * 4)
        zero_tex   = tuple([(0.0, 0.0)] * 4)
        zero_color = tuple([(1.0, 1.0, 1.0)] * 4)
        self.northWall = lambda x, y, z, w, h: (zero_quad, zero_tex, zero_color)
        self.westWall = lambda x, y, z, w, h: (zero_quad, zero_tex, zero_color)

    def floor(self, x: int, y: int, z: int, w: float, h: float) -> tuple: 
        # build vertices "on the ground"
        tl = (x*w + 0.0, z*h, y*w + 0.0)
        tr = (x*w +   w, z*h, y*w + 0.0)
        br = (x*w +   w, z*h, y*w +   w)
        bl = (x*w + 0.0, z*h, y*w +   w)
        vertices = (tl, tr, br, bl)
        # build texture coordinates
        tl = (0.0, 0.0)
        tr = (1.0, 0.0)
        br = (1.0, 0.5)
        bl = (0.0, 0.5)
        texcoords = (tl, tr, br, bl)
        # build colors
        tl = (1.0, 1.0, 1.0)
        tr = (1.0, 1.0, 1.0)
        br = (1.0, 1.0, 1.0)
        bl = (1.0, 1.0, 1.0)
        colors = (tl, tr, br, bl)
        return vertices, texcoords, colors

    def northWall(self, x: int, y: int, z: int, w: float, h: float) -> tuple:
        # build vertices "at the northern edge"
        bl = (x*w +  .0, 0.0 + z*h, y*w + 0.0)
        br = (x*w +   w, 0.0 + z*h, y*w + 0.0)
        tr = (x*w +   w,   h + z*h, y*w + 0.0)
        tl = (x*w + 0.0,   h + z*h, y*w + 0.0)
        vertices = (tl, tr, br, bl)
        # build texture coordinates
        tl = (0.0, 0.5)
        tr = (1.0, 0.5)
        br = (1.0, 1.0)
        bl = (0.0, 1.0)
        texcoords = (tl, tr, br, bl)
        # build colors
        tl = (1.0, 1.0, 1.0)
        tr = (1.0, 1.0, 1.0)
        br = (1.0, 1.0, 1.0)
        bl = (1.0, 1.0, 1.0)
        colors = (tl, tr, br, bl)
        return vertices, texcoords, colors
    
    def southWall(self, x: int, y: int, z: int, w: float, h: float) -> tuple:
        # build vertices "at the southern edge"
        return self.northWall(x, y+1, z, w, h)
    
    def westWall(self, x: int, y: int, z: int, w: float, h: float) -> tuple:
        # build vertices "at the western edge"
        tl = (x*w,   h + z*h, y*w + 0.0)
        tr = (x*w,   h + z*h, y*w +   w)
        br = (x*w, 0.0 + z*h, y*w +   w)
        bl = (x*w, 0.0 + z*h, y*w + 0.0)
        vertices = (tl, tr, br, bl)
        # build texture coordinates
        tl = (0.0, 0.5)
        tr = (1.0, 0.5)
        br = (1.0, 1.0)
        bl = (0.0, 1.0)
        texcoords = (tl, tr, br, bl)
        # build colors
        tl = (1.0, 1.0, 1.0)
        tr = (1.0, 1.0, 1.0)
        br = (1.0, 1.0, 1.0)
        bl = (1.0, 1.0, 1.0)
        colors = (tl, tr, br, bl)
        return vertices, texcoords, colors

    def eastWall(self, x: int, y: int, z: int, w: float, h: float) -> tuple:
        # build vertices "at the eastern edge"
        return self.westWall(x+1, y, z, w, h)
    
    def loadFromDungeon(self, dungeon) -> bool:
        white = (1.0, 1.0, 1.0)
        black = (0.0, 0.0, 0.0)
        yellow = (1.0, 1.0, 0.0)

        data = list()
        for y in range(dungeon.size[1]):
            for x in range(dungeon.size[0]):
                cell = dungeon[(x, y)]
                if cell.isWall():
                    continue
                
                # query neighbor cells
                north = cell.getNeighbor(dungeon, (0, -1))
                south = cell.getNeighbor(dungeon, (0,  1))
                east  = cell.getNeighbor(dungeon, ( 1, 0))
                west  = cell.getNeighbor(dungeon, (-1, 0))
                
                if cell.isFloor():
                    v, t, c = self.floor(x, y, 0, 3.0, 2.0)
                    data.append((v, t, c))

                if not cell.isWall():
                    if north.isWall():
                        v, t, c = self.northWall(x, y, 0, 3.0, 2.0)
                        data.append((v, t, c))
                    if south.isWall():
                        v, t, c = self.southWall(x, y, 0, 3.0, 2.0)
                        data.append((v, t, c))
                    if west.isWall():
                        v, t, c = self.westWall(x, y, 0, 3.0, 2.0)
                        data.append((v, t, c))
                    if east.isWall():
                        v, t, c = self.eastWall(x, y, 0, 3.0, 2.0)
                        data.append((v, t, c))

                if cell.isVoid():
                    if not north.isVoid():
                        v, t, c = self.northWall(x, y, -1, 3.0, 2.0)
                        c = (c[0], c[1], black, black)
                        data.append((v, t, c))
                    if not south.isVoid():
                        v, t, c = self.southWall(x, y, -1, 3.0, 2.0)
                        c = (c[0], c[1], black, black)
                        data.append((v, t, c))
                    if not west.isVoid():
                        v, t, c = self.westWall(x, y, -1, 3.0, 2.0)
                        c = (c[0], c[1], black, black)
                        data.append((v, t, c))
                    if not east.isVoid():
                        v, t, c = self.eastWall(x, y, -1, 3.0, 2.0) 
                        c = (c[0], c[1], black, black)
                        data.append((v, t, c))
        self.data = data
        return True

# ---------------------------------------------------------------------

class Cell(object):
    def __init__(self, x: int, y: int, symbol: str):
        self.pos      = (x, y)
        self.symbol   = symbol
        self.vertices = list()

        self.content = list()
    
    @staticmethod
    def Void(*args, **kwargs):
        kwargs['symbol'] = ' '
        return Cell(*args, **kwargs)
    
    @staticmethod
    def Wall(*args, **kwargs):
        kwargs['symbol'] = '#'
        return Cell(*args, **kwargs)

    @staticmethod
    def Floor(*args, **kwargs):
        kwargs['symbol'] = '.'
        return Cell(*args, **kwargs)

    def isVoid(self) -> bool:
        return self.symbol == ' '

    def isWall(self) -> bool:
        return self.symbol == '#'

    def isFloor(self) -> bool:
        return self.symbol == '.'
    
    def isWalkable(self) -> bool:
        # @NOTE: e.g. a door is not walkable as long as closed
        return self.isFloor() or self.isVoid()

    def isSolid(self) -> bool:
        # @NOTE: e.g. floor or a metal grate are "solid"
        return not self.isVoid()
    
    def getNeighbor(self, parent_dungeon, direction: tuple):
        """ Returns neighbor cell inside parent_dungeon in the given
        direciton.
        """   
        x = self.pos[0] + direction[0]
        y = self.pos[1] + direction[1]
        return parent_dungeon[(x, y)]


# --------------------------------------------------------------------- 

class Dungeon(object):
    def __init__(self):
        self.size  = (0, 0)
        self.cells = list()

    def resize(self, w: int, h: int):
        self.size = (w, h)
        # rebuild all cells
        self.cells = [Cell.Void(x=None, y=None)] * w * h

    def has(self, x: int, y: int) -> bool:
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def mapIndex(self, x: int, y: int):
        if not self.has(x, y):
            return -1
        # map 2d coord to 1d index using dungeon's size
        return y * self.size[0] + x

    def __getitem__(self, pos):
        """ e.g. obj[(2, 3)]
        """
        i = self.mapIndex(*pos)
        if i > -1:
            return self.cells[i]
        return Cell.Wall(*pos)

    def __setitem__(self, pos, cell) -> None:
        """ e.g. obj[(2, 3)] = foo
        """
        i = self.mapIndex(*pos)
        if i > -1:
            self.cells[i] = cell
        else:
            raise KeyError('Invalid dungeon position <{0}|{1}>'.format(*pos))

    def loadFromMemory(self, raw: str) -> bool:
        lines = raw.split('\n')
        
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
                d[(x, y)] = Cell(x, y, symbol)
                x += 1
            y += 1

        self.size  = d.size
        self.cells = d.cells

        return True

    def loadFromFile(self, fname: str) -> bool:
        with open(fname, 'r') as h:
            return self.loadFromMemory(h.read())

    def saveToMemory(self) -> str:
        # dump to ascii
        raw = '{0}x{1}'.format(*self.size)
        for i, cell in enumerate(self.cells):
            if i % self.size[0] == 0:
                raw += '\n'
            raw += cell.symbol
        return raw
        
    def saveToFile(self, fname: str) -> None:
        with open(fname, 'w') as h:
            h.write(self.saveToMemory())

