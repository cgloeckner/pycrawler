#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import unittest, tempfile

import pygame
import OpenGL.GL as gl 
import OpenGL.GLU as glu

from PIL import Image

import draw


class OpenGLTest(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((640, 480), pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)

    def ortho(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, 640, 480, 0.0, -0.01, 10.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def perspective(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, 640/480, 0.1, 30.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()         
        gl.glEnable(gl.GL_DEPTH_TEST)
        
    def tearDown(self):
        pygame.quit()


# ---------------------------------------------------------------------

class TextureTest(OpenGLTest):
    
    def test_ctor(self):
        t = draw.Texture()
        self.assertIsNone(t.id)
        self.assertEqual(t.w, 0)
        self.assertEqual(t.h, 0)

    def test_loadFromFile(self):
        t = draw.Texture()

        # create dummy texture and load into texture
        img = Image.new(mode='RGB', size=(150, 80))
        with tempfile.NamedTemporaryFile('wb') as h:
            img.save(h.name, 'PNG')
            self.assertTrue(t.loadFromFile(h.name))


# ---------------------------------------------------------------------

class Sprite2DTest(OpenGLTest):

    def test_ctor(self):
        s = draw.Sprite2D()
        self.assertEqual(s.x, 0)
        self.assertEqual(s.y, 0)
        self.assertEqual(s.w, 1.0)
        self.assertEqual(s.h, 1.0)

        self.assertEqual(len(s.vertices), 4)
        self.assertEqual(s.vertices[0], (0.0, 0.0, 0.0))
        self.assertEqual(s.vertices[1], (1.0, 0.0, 0.0))
        self.assertEqual(s.vertices[2], (1.0, 1.0, 0.0))
        self.assertEqual(s.vertices[3], (0.0, 1.0, 0.0))

        # color: white
        self.assertEqual(len(s.color), 4)
        for i in range(4):
            self.assertEqual(s.color[i], (1.0, 1.0, 1.0))

        # texture not initialized
        self.assertIsNone(s.texture)
        self.assertEqual(s.texrect, (0.0, 0.0, 1.0, 1.0))
        self.assertEqual(len(s.texcoords), 4)
        self.assertEqual(s.texcoords[0], (0.0, 0.0))
        self.assertEqual(s.texcoords[1], (1.0, 0.0))
        self.assertEqual(s.texcoords[2], (1.0, 1.0))
        self.assertEqual(s.texcoords[3], (0.0, 1.0))

        # rendering does not crash
        self.ortho()
        s.render()

    def test_moveTo(self):
        s = draw.Sprite2D()
        s.moveTo(400, 300)
         
        # rendering does not crash
        self.ortho()
        s.render()

    def test_moveBy(self):
        s = draw.Sprite2D()
        s.moveBy(400, 300)
        s.moveBy(-200, -180)
        self.assertEqual(s.x, 200)
        self.assertEqual(s.y, 120)
         
        # rendering does not crash
        self.ortho()
        s.render()

    def test_resize(self):
        s = draw.Sprite2D()
        s.resize(200, 80)
        self.assertEqual(s.w, 200)
        self.assertEqual(s.h, 80)

        # expect vertices to be built
        self.assertEqual(len(s.vertices), 4)
        self.assertEqual(s.vertices[0], (  0.0,  0.0, 0.0)) # topleft
        self.assertEqual(s.vertices[1], (200.0,  0.0, 0.0)) # topright
        self.assertEqual(s.vertices[2], (200.0, 80.0, 0.0)) # bottomright
        self.assertEqual(s.vertices[3], (  0.0, 80.0, 0.0)) # bottomleft
        
        # rendering does not crash 
        self.ortho()
        s.render()

    def test_colorize(self):
        s = draw.Sprite2D()
        red   = (1.0, 0.0, 0.0)
        green = (0.0, 1.0, 0.0)
        blue  = (0.0, 0.0, 1.0)
        white = (1.0, 1.0, 1.0)

        # use tuple of colors
        s.colorize(red, green, blue, white)
        self.assertEqual(s.color[0], red)
        self.assertEqual(s.color[1], green)
        self.assertEqual(s.color[2], blue)
        self.assertEqual(s.color[3], white)
        self.ortho()
        s.render()

        # use single color
        s.colorize(green)
        for i in range(4):
            self.assertEqual(s.color[i], green)
        self.ortho()
        s.render()

    def test_clip(self):
        s = draw.Sprite2D()
        s.clip(0.5, 0.2, 0.4, 0.35)
        self.assertEqual(s.texrect, (0.5, 0.2, 0.4, 0.35))

        # expect texcoords to be built
        self.assertEqual(len(s.texcoords), 4)
        self.assertEqual(s.texcoords[0], (0.5, 0.2 )) # topleft
        self.assertEqual(s.texcoords[1], (0.9, 0.2 )) # topright
        self.assertEqual(s.texcoords[2], (0.9, 0.55)) # bottomright
        self.assertEqual(s.texcoords[3], (0.5, 0.55)) # bottomleft
        
        # rendering does not crash (even without a texture)
        self.ortho()
        s.render()

    def test_render(self):
        t = draw.Texture()

        # create dummy texture and load into texture
        img = Image.new(mode='RGB', size=(150, 80))
        with tempfile.NamedTemporaryFile('wb') as h:
            img.save(h.name, 'PNG')
            self.assertTrue(t.loadFromFile(h.name))

        # create sprite using that texture
        s = draw.Sprite2D()
        s.texture = t
        s.clip(0.5, 0.2, 0.4, 0.35)

        # rendering does not crash 
        self.ortho()
        s.render()
