#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import unittest
import pygame
import OpenGL.GL as gl 
import OpenGL.GLU as glu


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

