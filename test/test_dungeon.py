#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import unittest, tempfile

import dungeon



class VertexBuilderTest(unittest.TestCase):

    def test_floor(self):
        v, t, c = dungeon.VertexBuilder.floor(4, 5, 3.0, 2.0)
        self.assertEqual(len(v), 4)
        # square floor in xz-plane
        self.assertEqual(v[0], (12.0, 0.0, 15.0))
        self.assertEqual(v[1], (15.0, 0.0, 15.0))
        self.assertEqual(v[2], (15.0, 0.0, 18.0))
        self.assertEqual(v[3], (12.0, 0.0, 18.0))
        # texCoord for floor rect
        self.assertEqual(t[0], (0.0, 0.0))
        self.assertEqual(t[1], (1.0, 0.0))
        self.assertEqual(t[2], (1.0, 0.5))
        self.assertEqual(t[3], (0.0, 0.5))
        # white color for all vertices
        for i in range(4):
            self.assertEqual(c[i], (1.0, 1.0, 1.0))
    
    def test_northWall(self):
        v, t, c = dungeon.VertexBuilder.northWall(4, 5, 3.0, 2.0, z=-1)
        self.assertEqual(len(v), 4)
        # rect wall in far xy-plane
        self.assertEqual(v[0], (12.0,  0.0, 15.0))
        self.assertEqual(v[1], (15.0,  0.0, 15.0))
        self.assertEqual(v[2], (15.0, -2.0, 15.0))
        self.assertEqual(v[3], (12.0, -2.0, 15.0)) 
        # texCoord for wall rect
        self.assertEqual(t[0], (0.0, 0.5))
        self.assertEqual(t[1], (1.0, 0.5))
        self.assertEqual(t[2], (1.0, 1.0))
        self.assertEqual(t[3], (0.0, 1.0))
        # white color for all vertices
        for i in range(4):
            self.assertEqual(c[i], (1.0, 1.0, 1.0))

    def test_southWall(self):
        v, t, c = dungeon.VertexBuilder.southWall(4, 5, 3.0, 2.0, z=-1)
        self.assertEqual(len(v), 4)
        # rect wall in close xy-plane
        self.assertEqual(v[0], (12.0,  0.0, 18.0))
        self.assertEqual(v[1], (15.0,  0.0, 18.0))
        self.assertEqual(v[2], (15.0, -2.0, 18.0))
        self.assertEqual(v[3], (12.0, -2.0, 18.0)) 
        # texCoord for wall rect
        self.assertEqual(t[0], (0.0, 0.5))
        self.assertEqual(t[1], (1.0, 0.5))
        self.assertEqual(t[2], (1.0, 1.0))
        self.assertEqual(t[3], (0.0, 1.0))
        # white color for all vertices
        for i in range(4):
            self.assertEqual(c[i], (1.0, 1.0, 1.0))
    
    def test_westWall(self):
        v, t, c = dungeon.VertexBuilder.westWall(4, 5, 3.0, 2.0, z=-1)
        self.assertEqual(len(v), 4)
        # rect wall in left-hand yz-plane
        self.assertEqual(v[0], (12.0,  0.0, 15.0))
        self.assertEqual(v[1], (12.0,  0.0, 18.0))
        self.assertEqual(v[2], (12.0, -2.0, 18.0))
        self.assertEqual(v[3], (12.0, -2.0, 15.0)) 
        # texCoord for wall rect
        self.assertEqual(t[0], (0.0, 0.5))
        self.assertEqual(t[1], (1.0, 0.5))
        self.assertEqual(t[2], (1.0, 1.0))
        self.assertEqual(t[3], (0.0, 1.0))
        # white color for all vertices
        for i in range(4):
            self.assertEqual(c[i], (1.0, 1.0, 1.0))
    
    def test_eastWall(self):
        v, t, c = dungeon.VertexBuilder.eastWall(4, 5, 3.0, 2.0, z=-1)
        self.assertEqual(len(v), 4)
        # rect wall in left-hand yz-plane
        self.assertEqual(v[0], (15.0,  0.0, 15.0))
        self.assertEqual(v[1], (15.0,  0.0, 18.0))
        self.assertEqual(v[2], (15.0, -2.0, 18.0))
        self.assertEqual(v[3], (15.0, -2.0, 15.0)) 
        # texCoord for wall rect
        self.assertEqual(t[0], (0.0, 0.5))
        self.assertEqual(t[1], (1.0, 0.5))
        self.assertEqual(t[2], (1.0, 1.0))
        self.assertEqual(t[3], (0.0, 1.0))
        # white color for all vertices
        for i in range(4):
            self.assertEqual(c[i], (1.0, 1.0, 1.0))


# ---------------------------------------------------------------------

class CellTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_init_aliases(self):
        void_cell  = dungeon.Cell.Void(x=0, y=4)
        wall_cell  = dungeon.Cell.Wall(x=1, y=5)
        floor_cell = dungeon.Cell.Floor(x=2, y=6)

        self.assertEqual(void_cell.pos, (0, 4))
        self.assertEqual(wall_cell.pos, (1, 5))
        self.assertEqual(floor_cell.pos, (2, 6))

        self.assertTrue(void_cell.isVoid())
        self.assertFalse(void_cell.isWall())
        self.assertFalse(void_cell.isFloor())

        self.assertFalse(wall_cell.isVoid())
        self.assertTrue(wall_cell.isWall())
        self.assertFalse(wall_cell.isFloor())

        self.assertFalse(floor_cell.isVoid())
        self.assertFalse(floor_cell.isWall())
        self.assertTrue(floor_cell.isFloor())

    def test_getNeighbor(self):
        # load test dungeon
        raw = '''3x3
#.#
. #
# #'''
        d = dungeon.Dungeon()
        self.assertTrue(d.loadFromMemory(raw))

        center = d[(1, 1)]
        north  = center.getNeighbor(d, ( 0, -1))
        south  = center.getNeighbor(d, ( 0,  1))
        east   = center.getNeighbor(d, ( 1,  0))
        west   = center.getNeighbor(d, (-1,  0))

        self.assertTrue(north.isVoid())
        self.assertTrue(south.isFloor())
        self.assertTrue(east.isWall())
        self.assertTrue(west.isVoid())


# ---------------------------------------------------------------------

class DungeonTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_init(self):
        d = dungeon.Dungeon()
        self.assertEqual(d.size, (0, 0))
        self.assertEqual(d.cells, list())

    def test_resize(self):
        d = dungeon.Dungeon()

        # resize fills with void
        d.resize(5, 10)
        self.assertEqual(d.size, (5, 10))
        self.assertEqual(len(d.cells), 5*10)
        for c in d.cells:
            self.assertTrue(c.isVoid())

        # resize resets all cells
        for c in d.cells:
            c = dungeon.Cell.Floor(x=0, y=0)
        d.resize(7, 12)
        self.assertEqual(d.size, (7, 12))
        self.assertEqual(len(d.cells), 7*12)
        for c in d.cells:
            self.assertTrue(c.isVoid())

    def test_has(self): 
        d = dungeon.Dungeon()
        d.resize(3, 4)
        self.assertTrue(d.has(0, 0))
        self.assertTrue(d.has(2, 0))
        self.assertTrue(d.has(2, 3))
        self.assertTrue(d.has(0, 3))
        
        self.assertFalse(d.has(-1, 0))
        self.assertFalse(d.has(0, -1))
        self.assertFalse(d.has(3, 0))
        self.assertFalse(d.has(0, 4))

    def test_mapIndex(self):
        d = dungeon.Dungeon()
        d.resize(3, 4)
        self.assertEqual(d.mapIndex(0, 0), 0)
        self.assertEqual(d.mapIndex(1, 0), 1)
        self.assertEqual(d.mapIndex(2, 0), 2)
        self.assertEqual(d.mapIndex(3, 0), -1)

        self.assertEqual(d.mapIndex(0, 1), 3)
        self.assertEqual(d.mapIndex(1, 1), 4)
        self.assertEqual(d.mapIndex(2, 3), 11)
    
    def test_get_set(self):
        d = dungeon.Dungeon()
        d.resize(3, 4)
        
        d[(2, 3)] = dungeon.Cell.Floor(x=0, y=0)
        
        self.assertTrue(d[(2, 3)].isFloor())

    def test_loadFromMemory_saveToMemory(self):
        # load from string
        raw = '5x3\n#####\n #..#\n#####'
        d = dungeon.Dungeon()
        self.assertTrue(d.loadFromMemory(raw))                    
        for c in d.cells:
            self.assertTrue(d.has(*c.pos))

        # save to string
        out = d.saveToMemory()
        self.assertEqual(raw, out)
        
    def test_loadFromFile_saveToFile(self):
        raw = '5x3\n#####\n #..#\n#####'
        d = dungeon.Dungeon()
        
        with tempfile.NamedTemporaryFile('w+') as tmp:
            # write file
            tmp.write(raw)
            tmp.flush()

            # load demo dungeon
            self.assertTrue(d.loadFromFile(tmp.name))
            for c in d.cells:
                self.assertTrue(d.has(*c.pos))

        with tempfile.NamedTemporaryFile('w+') as tmp:
            # save demo dungeon
            d.saveToFile(tmp.name)
            tmp.flush()

            # read file
            content = tmp.read()
            self.assertEqual(content, raw)
