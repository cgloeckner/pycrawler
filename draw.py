#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import pygame
import OpenGL.GL as gl


class Texture(object):
    def __init__(self):
        self.id = None
        self.w  = 0
        self.h  = 0

    def loadFromFile(self, fname):
        surface = pygame.image.load(fname).convert_alpha()
        data = pygame.image.tostring(surface, "RGBA", 1)
        self.w = surface.get_width()
        self.h = surface.get_height()

        gl.glEnable(gl.GL_TEXTURE_2D)
        self.id = gl.glGenTextures(1)
        self.bind()
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.w, self.h, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        
        return True

    @staticmethod
    def unbind():
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)


# ---------------------------------------------------------------------

class Sprite2D(object):
    def __init__(self, w=1.0, h=1.0):
        self.x = 0
        self.y = 0
        self.color = tuple([(1.0, 1.0, 1.0)] * 4) # topleft, tright, bottoml, br
        self.origin = (0.5, 0.5) # centered

        self.resize(w, h)
        
        self.texture = None
        self.clip(0.0, 0.0, 1.0, 1.0)

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def moveBy(self, dx, dy):
        self.x += dx
        self.y += dy

    def centerTo(self, relx, rely):
        self.origin = (relx, rely)

    def resize(self, w, h):
        w = float(w)
        h = float(h) 
        self.w = float(w)
        self.h = float(h)
        self.rebuild()

    def rebuild(self):
        # rebuild vertices
        tl = (   0.0,    0.0, 0.0)
        tr = (self.w,    0.0, 0.0)
        br = (self.w, self.h, 0.0)
        bl = (   0.0, self.h, 0.0)
        self.vertices = (tl, tr, br, bl)

    def colorize(self, *colors):
        """ Set either one color for all vertices by using a single
        argument or use four arguments to assign them to the vertices
        in order: topleft, topright, bottomright, bottomleft.
        """
        if len(colors) == 4:
            # apply individual color per vertex
            self.color = tuple(colors)
        else:
            # apply color for all vertices
            self.color = tuple([colors[0]] * 4)

    def clip(self, left, top, w, h):
        self.texrect = (left, top, w, h)
        # rebuild texture coordinates
        tl = (left,     top)
        tr = (left + w, top)
        br = (left + w, top + h)
        bl = (left    , top + h)
        self.texcoords = (tl, tr, br, bl)

    def transform(self):
        gl.glTranslate(self.x - self.origin[0] * self.w, self.y - self.origin[1] * self.h, 0.0)

    def render(self):
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        self.transform()

        if self.texture is not None:
            self.texture.bind()
        else:
            Texture.unbind()
        
        gl.glBegin(gl.GL_QUADS)
        for i in range(4):
            gl.glTexCoord2fv(self.texcoords[i])
            gl.glColor3fv(self.color[i])
            gl.glVertex3fv(self.vertices[i])
        gl.glEnd()
        
        gl.glPopMatrix()

