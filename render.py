#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import math

import pygame
import OpenGL.GL as gl


class CameraAnimation(object):
    def __init__(self, camera):
        self.camera = camera
        self.handle = None
        self.args   = list()
        self.counts = 0

    def start(self, handle, args, counts):
        self.handle = handle
        self.args   = args
        self.counts = counts

    def startAhead(self, direction):
        self.start(self.camera.move, (direction * 0.05, True), 1.0 / 0.05)
        
    def startSideways(self, direction):
        self.start(self.camera.move, (direction * 0.05, False), 1.0 / 0.05)
        
    def startRotate(self, direction):
        self.start(self.camera.rotate, (direction * 5.0, ), 90.0 / 5.0)

    def isIdle(self):
        return self.counts <= 0 or self.handle is None

    def __call__(self):
        if self.isIdle():
            return

        # trigger stored action and count down
        self.handle(*self.args)
        self.counts -= 1


# ---------------------------------------------------------------------

class Camera(object):
    def __init__(self, scale=1.0):
        """ `scale` refers to tilesize (e.g. if 3.0 is one tile), so
        all positions can be in world scale.
        """
        self.scale = scale
        self.moveTo(0.0, 0.0, 0.0)
        self.look  = (0.0, 1.0)
        self.angle = 180.0

        self.animation = CameraAnimation(self)
    
    def getLookNormal(self):
        # calculate normal vector of looking direction within xz-plane
        # x = x * cos(90°) - y * sin(90°)
        # y = x * sin(90°) + y * cos(90°)
        return (-self.look[1], self.look[0])

    def rotate(self, angle):
        """ Rotate around y-axis.
        """
        # x <- x * cos(alpha) - y * sin(alpha)
        # y <- x * sin(alpha) + y * cos(alpha)
        radians  = angle * math.pi / 180.0
        cosalpha = math.cos(radians)
        sinalpha = math.sin(radians)
        x, z = self.look
        newx = x * cosalpha - z * sinalpha
        newz = x * sinalpha + z * cosalpha
        self.look  = (newx, newz)
        self.angle = (self.angle + angle) % 360.0
    
    def moveTo(self, x: float, y: float, z: float):
        self.pos = (self.scale * x, self.scale * y, self.scale * z)

    def move(self, distance, ahead=True):
        into = self.look if ahead else self.getLookNormal()
        
        x, y, z = self.pos
        x += self.scale * distance * into[0]
        z += self.scale * distance * into[1]
        self.pos = (x, y, z)

    def moveUp(self, distance):
        x, y, z = self.pos
        y += self.scale * distance
        self.pos = (x, y, z)

    def apply(self):
        gl.glRotate(self.angle, 0.0, 1.0, 0.0)
        gl.glTranslate(-self.pos[0], -self.pos[1], -self.pos[2])
    
    def update(self, keys):
        """ Handle input key input
        """
        if self.animation.isIdle():
            if keys[pygame.K_w]:
                self.animation.startAhead(1)
                
            elif keys[pygame.K_s]:
                self.animation.startAhead(-1)
                
            elif keys[pygame.K_a]:
                self.animation.startSideways(-1)
                
            elif keys[pygame.K_d]:  
                self.animation.startSideways(1)
                
            elif keys[pygame.K_q]:
                self.animation.startRotate(-1)
                
            elif keys[pygame.K_e]:
                self.animation.startRotate(1)
        
        self.animation()

