#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

import math

from PIL import Image

from test.utils import OpenGLTest

import render


class CameraAnimationTest(OpenGLTest):
    
    def test_init(self):
        ani = render.CameraAnimation(render.Camera())

        self.assertIsNotNone(ani.camera)
        self.assertIsNone(ani.handle)
        self.assertEqual(ani.args, list())
        self.assertEqual(ani.counts, 0)
        self.assertTrue(ani.isIdle())

    def test_start_call_idle(self):
        class Test(object):
            def __init__(self):
                self.i = 0
            def foo(self, n):
                self.i += n

        t = Test()
        ani = render.CameraAnimation(render.Camera())
        ani.start(t.foo, (2, ), 13)
        
        self.assertEqual(ani.handle, t.foo)
        self.assertEqual(ani.args, (2, ))
        self.assertEqual(ani.counts, 13)

        ani()
        self.assertEqual(t.i, 2)
        self.assertEqual(ani.counts, 12)
        self.assertFalse(ani.isIdle())

        for i in range(ani.counts-1):
            ani()
            self.assertFalse(ani.isIdle())
        
        self.assertEqual(t.i, 24)
        self.assertEqual(ani.counts, 1)

        ani()
        self.assertEqual(t.i, 26)
        self.assertEqual(ani.counts, 0) 
        self.assertTrue(ani.isIdle())

        # cannot execute further
        ani()
        self.assertEqual(t.i, 26)
        self.assertEqual(ani.counts, 0) 
        self.assertTrue(ani.isIdle())

        # restart
        t = Test()
        ani = render.CameraAnimation(render.Camera())
        ani.start(t.foo, (3, ), 2)
        
        self.assertEqual(ani.handle, t.foo)
        self.assertEqual(ani.args, (3, ))
        self.assertEqual(ani.counts, 2)

        ani()
        self.assertEqual(t.i, 3)
        self.assertEqual(ani.counts, 1)
        self.assertFalse(ani.isIdle())

    def test_start_aliases(self):
        cam = render.Camera()
        ani = render.CameraAnimation(cam)

        ani.startAhead(1)
        self.assertEqual(ani.handle, cam.move)
        self.assertEqual(ani.args, (0.05, True))
        self.assertEqual(ani.counts, 20)
        ani()
        
        ani.startAhead(-1)
        self.assertEqual(ani.handle, cam.move)
        self.assertEqual(ani.args, (-0.05, True))
        self.assertEqual(ani.counts, 20) 
        ani()

        ani.startSideways(1)
        self.assertEqual(ani.handle, cam.move)
        self.assertEqual(ani.args, (0.05, False))
        self.assertEqual(ani.counts, 20)
        ani()
        
        ani.startSideways(-1)
        self.assertEqual(ani.handle, cam.move)
        self.assertEqual(ani.args, (-0.05, False))
        self.assertEqual(ani.counts, 20)  
        ani()

        ani.startRotate(1)
        self.assertEqual(ani.handle, cam.rotate)
        self.assertEqual(ani.args, (5.0, ))
        self.assertEqual(ani.counts, 18) 
        ani()
        
        ani.startRotate(-1)
        self.assertEqual(ani.handle, cam.rotate)
        self.assertEqual(ani.args, (-5.0, ))
        self.assertEqual(ani.counts, 18) 
        ani()


# ---------------------------------------------------------------------

class CameraTest(OpenGLTest):
    
    def test_init(self):
        c = render.Camera(2.5)

        self.assertAlmostEqual(c.scale, 2.5)  
        self.assertAlmostEqual(c.pos, (0.0, 0.0, 0.0))
        self.assertAlmostEqual(c.angle, 180.0)
        self.assertAlmostEqual(c.look, (0.0, 1.0))

        # applying does not crash
        c.apply()

    def test_getLookNormal(self): 
        c = render.Camera(2.5)
        normal = c.getLookNormal()
        self.assertEqual(normal[0], -1)
        self.assertEqual(normal[1],  0)

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

    def test_move(self):
        # move ahead
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.move(0.5, ahead=True)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5 + 0.5*2.5)
        
        # applying does not crash
        c.apply()
        
        # rotate 90° to the right and move ahead
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.rotate(90.0)
        self.assertAlmostEqual(c.look[0], -1.0)
        self.assertAlmostEqual(c.look[1],  0.0)
        c.move(0.5, ahead=True)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5 - 0.5*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)

        # applying does not crash
        c.apply()

        # move sideways
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.move(0.5, ahead=False)
        
        self.assertAlmostEqual(c.pos[0], 1.2*2.5 - 0.5*2.5)
        self.assertAlmostEqual(c.pos[1], 3.4*2.5)
        self.assertAlmostEqual(c.pos[2], 5.6*2.5)
        
        # rotate 90° to the right and move sideways
        c = render.Camera(2.5)
        c.moveTo(1.2, 3.4, 5.6)
        c.rotate(90.0)          
        self.assertAlmostEqual(c.look[0], -1.0)
        self.assertAlmostEqual(c.look[1],  0.0)
        c.move(0.5, ahead=False)
         
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

    def test_update(self):
        # prepare key stuff
        import pygame
        
        move_keys = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
        rotate_keys = [pygame.K_q, pygame.K_e]

        def buildKeyMap(*args):
            data = {}
            for key in move_keys:
                data[key] = False
            for key in rotate_keys:
                data[key] = False
            for key in args:
                data[key] = True
            return data

        # nothing happens on idle
        c = render.Camera(2.5)
        c.update(pygame.key.get_pressed())
        self.assertTrue(c.animation.isIdle())

        # test moving 
        for key in move_keys:
            c = render.Camera(2.5)
            c.update(buildKeyMap(key))
            self.assertEqual(c.animation.handle, c.move)
            args = c.animation.args
            self.assertFalse(c.animation.isIdle())
            
            # other input is ignored
            for other in move_keys:
                if key == other:
                    continue
                c.update(buildKeyMap(key))
                self.assertEqual(c.animation.handle, c.move)
                self.assertEqual(c.animation.args, args)
            for other in rotate_keys:
                c.update(buildKeyMap(key))
                self.assertEqual(c.animation.handle, c.move)

        # test rotating
        for key in rotate_keys:
            c = render.Camera(2.5)
            c.update(buildKeyMap(key))
            self.assertEqual(c.animation.handle, c.rotate)
            args = c.animation.args
            self.assertFalse(c.animation.isIdle())
            
            # other input is ignored
            for other in rotate_keys:
                if key == other:
                    continue
                c.update(buildKeyMap(key))
                self.assertEqual(c.animation.handle, c.rotate)
                self.assertEqual(c.animation.args, args)
            for other in move_keys: 
                c.update(buildKeyMap(key))
                self.assertEqual(c.animation.handle, c.rotate)



