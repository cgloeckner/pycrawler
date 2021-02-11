#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu

import dungeon, draw, render

"""
def createMinimap(tileset, dungeon, tile_size):
    minimap = pygame.Surface((dungeon.size[0] * tile_size, dungeon.size[1] * tile_size))
    for y in range(dungeon.size[1]):
        for x in range(dungeon.size[0]):
            cell = dungeon.get(x, y)
            tex_coords = cell.getTexCoords()
            if tex_coords is None:
                continue # nothing to draw for Void
            # blit to minimap
            src = pygame.Rect((int)(tex_coords[0][0] * tile_size), (int)(tex_coords[0][1] * tile_size * 2), tile_size, tile_size)
            dst = pygame.Rect(cell.pos[0] * tile_size, cell.pos[1] * tile_size, tile_size, tile_size)
            minimap.blit(tileset, dst, src)
    return minimap
"""



class Renderer(object):
    def __init__(self, w, h):
        self.resolution = (w, h)
        self.screen     = pygame.display.set_mode((w, h), pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)
        self.cam        = None

        # enable alpha from RGBA texture
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glAlphaFunc(gl.GL_NOTEQUAL, 0.0)

    def loadDungeon(self, dungeon):
        self.cam = render.Camera(dungeon, 3.0)
        self.cam.moveTo(1.5, 0.175, 1.5)
        #self.cam.no_collision = True

    def ortho(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, self.resolution[0], self.resolution[1], 0.0, -0.01, 10.0)

        # @NOTE: this reverts the workaround inside perspective()
        gl.glMatrixMode(gl.GL_TEXTURE)
        gl.glLoadIdentity()
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def perspective(self):
        assert(self.cam is not None)
        
        self.aspect_ratio = self.resolution[0] / self.resolution[1]
        
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, self.aspect_ratio, 0.1, 30.0)
        self.cam.apply()

        # @WORKAROUND: this y-flips all texture to be shown correctly.
        gl.glMatrixMode(gl.GL_TEXTURE)
        gl.glLoadIdentity()
        gl.glScale(1.0, -1.0, 1.0) 
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()         
        gl.glEnable(gl.GL_DEPTH_TEST)

    def clear(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def update(self):
        pygame.display.flip()




# ---------------------------------------------------------------------
           

if __name__ == '__main__':
    pygame.init()
    renderer = Renderer(640, 480) 
    running  = True
    
    fpsclock = pygame.time.Clock()

    tileset = draw.Texture()
    tileset.loadFromFile('tileset.png')

    heart = draw.Texture()
    heart.loadFromFile('heart.png')

    potion = draw.Texture()
    potion.loadFromFile('potion.png')
    
    #minimap = createMinimap(tileset, d, 16)

    hud = draw.Sprite2D(32, 32)
    hud.moveTo(640, 480)
    hud.centerTo(1.0, 1.0)
    hud.texture = heart

    # demo terrain
    d = dungeon.Dungeon()
    d.loadFromFile('demo.txt')
    renderer.loadDungeon(d)

    vb = dungeon.VertexBuilder()
    #vb.no_walls()
    vb.loadFromDungeon(d)

    next_fps_update = 0

    sprite1 = draw.Sprite3D()
    sprite1.resize(0.5, 0.5)
    sprite1.moveTo(4.5, 0.0, 4.5)
    sprite1.centerTo(0.5, 0.0, 0.5)
    sprite1.texture = potion
    
    sprite2 = draw.Sprite3D()
    sprite2.resize(0.5, 0.5)
    sprite2.moveTo(5.0, 0.0, 4.0)
    sprite2.centerTo(0.5, 0.0, 0.5)
    sprite2.texture = potion
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        renderer.cam.update(pygame.key.get_pressed())

        renderer.clear()
        
        renderer.ortho()
        hud.render()

        renderer.perspective()
        
        # draw terrain
        tileset.bind()
        gl.glBegin(gl.GL_QUADS)
        for v, t, c in vb.data:
            for i in range(4):
                gl.glColor3fv(c[i])
                gl.glTexCoord2fv(t[i])
                gl.glVertex3fv(v[i])
        gl.glEnd()
        
        sprite1.rotate = renderer.cam.angle
        sprite2.rotate = renderer.cam.angle
        
        sprite1.render()
        sprite2.render()
        
        #screen.blit(minimap, (50, 50))
        renderer.update()
        fpsclock.tick(60)

    pygame.quit()
