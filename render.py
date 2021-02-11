#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import math
import OpenGL.GL as gl


class Camera(object):
    def __init__(self, scale=1.0):
        """ `scale` refers to tilesize (e.g. if 3.0 is one tile), so
        all positions can be in world scale.
        """
        self.scale = scale
        self.moveTo(0.0, 0.0, 0.0)
        self.look  = (0.0, 1.0)
        self.angle = 180.0

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
        self.look   = (newx, newz)
        self.angle += angle
    
    def moveTo(self, x: float, y: float, z: float):
        self.pos = (self.scale * x, self.scale * y, self.scale * z)

    def moveAhead(self, distance):
        x, y, z = self.pos
        x += self.scale * distance * self.look[0]
        z += self.scale * distance * self.look[1]
        self.pos = (x, y, z)

    def moveSideways(self, distance):
        # calculate normal vector of looking direction within xz-plane
        # x = x * cos(90°) - y * sin(90°)
        # y = x * sin(90°) + y * cos(90°)
        normal_x = -self.look[1]
        normal_z =  self.look[0]

        # alter position       
        x, y, z = self.pos
        x += self.scale * distance * normal_x
        z += self.scale * distance * normal_z  
        self.pos = (x, y, z)

    def moveUp(self, distance):
        x, y, z = self.pos
        y += self.scale * distance
        self.pos = (x, y, z)

    def apply(self):
        gl.glRotate(self.angle, 0.0, 1.0, 0.0)
        gl.glTranslate(-self.pos[0], -self.pos[1], -self.pos[2])

