#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import unittest, tempfile

import dungeon


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

    def test_getTexCoords(self):
        void_cell  = dungeon.Cell.Void(x=0, y=4)
        wall_cell  = dungeon.Cell.Wall(x=1, y=5)
        floor_cell = dungeon.Cell.Floor(x=2, y=6)

        self.assertIsNone(void_cell.getTexCoords())

        wall_coords = wall_cell.getTexCoords()
        self.assertEqual(wall_coords[0], (0.0, 0.5)) # top left
        self.assertEqual(wall_coords[1], (1.0, 0.5)) # top right
        self.assertEqual(wall_coords[2], (1.0, 1.0)) # bottom right
        self.assertEqual(wall_coords[3], (0.0, 1.0)) # bottom left
        
        floor_coords = floor_cell.getTexCoords()
        self.assertEqual(floor_coords[0], (0.0, 0.0)) # top left
        self.assertEqual(floor_coords[1], (1.0, 0.0)) # top right
        self.assertEqual(floor_coords[2], (1.0, 0.5)) # bottom right
        self.assertEqual(floor_coords[3], (0.0, 0.5)) # bottom left


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
        with self.assertRaises(KeyError):
            d.mapIndex(3, 0)

        self.assertEqual(d.mapIndex(0, 1), 3)
        self.assertEqual(d.mapIndex(1, 1), 4)
        self.assertEqual(d.mapIndex(2, 3), 11)
    
    def test_get_set(self):
        d = dungeon.Dungeon()
        d.resize(3, 4)
        
        d.set(2, 3, dungeon.Cell.Floor(x=0, y=0))
        
        self.assertTrue(d.get(2, 3).isFloor())

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
