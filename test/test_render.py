#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import math

from PIL import Image

import render
from test.utils import OpenGLTest


class CameraTest(OpenGLTest):
    
    def test_init(self):
        c = render.Camera(2.5)

        self.assertAlmostEqual(c.scale, 2.5)  
        self.assertAlmostEqual(c.pos, (0.0, 0.0, 0.0))
        self.assertAlmostEqual(c.angle, 180.0)
        self.assertAlmostEqual(c.look, (0.0, 1.0))

        # applying does not crash
        c.apply()
    
    def test_rotate(self):
        c = render.Camera(2.5)
        prev = c.look
        c.rotate(45.0) 
        self.assertAlmostEqual(c.angle, 225.0) # base angle == 180

        # x == x * cos(alpha) - y * sin(alpha)
        # y == x * sin(alpha) + y * cos(alpha)
        radians  = 45.0 * math.pi / 180.0
        cosalpha = math.cos(radians)
        sinalpha = math.sin(radians)
        self.assertAlmostEqual(c.look[0], prev[0] * cosalpha - prev[1] * sinalpha)
        self.assertAlmostEqual(c.look[1], prev[0] * sinalpha + prev[1] * cosalpha)

        # continue rotation
        prev = c.look 
        c.rotate(-130.0)
        self.assertAlmostEqual(c.angle, 95.0)
        
        radians  = -130.0 * math.pi / 180.0
        cosalpha = math.cos(radians)
        sinalpha = math.sin(radians)
        self.assertAlmostEqual(c.look[0], prev[0] * cosalpha - prev[1] * sinalpha)
        self.assertAlmostEqual(c.look[1], prev[0] * sinalpha + prev[1] * cosalpha)

        # applying does not crash
        c.apply()

    def test_moveTo(self):
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)

        self.assertAlmostEqual(c.pos[0], 1.2*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)

        # applying does not crash
        c.apply()

    def test_moveAhead(self):
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.moveAhead(0.5)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5 + 0.5*2.5)

        # rotate 90° to the right 
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.rotate(90.0)
        self.assertAlmostEqual(c.look[0], -1.0)
        self.assertAlmostEqual(c.look[1],  0.0)
        c.moveAhead(0.5)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5 - 0.5*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)

        # applying does not crash
        c.apply()

    def test_moveSideways(self):
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.moveSideways(0.5)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5 - 0.5*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)
        
        # rotate 90° to the right 
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.rotate(90.0)          
        self.assertAlmostEqual(c.look[0], -1.0)
        self.assertAlmostEqual(c.look[1],  0.0)
        c.moveSideways(0.5)
         
        self.assertAlmostEqual(c.pos[0], 1.2*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5 - 0.5*2.5)

        # applying does not crash
        c.apply()

    def test_moveUp(self):
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.moveUp(7.8)

        self.assertAlmostEqual(c.pos[0], 1.2*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5 + 7.8*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)

        # applying does not crash
        c.apply()


 
