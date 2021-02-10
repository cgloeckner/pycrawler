#!/usr/bin/python3 
# -*- coding: utf-8 -*-

import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu

import dungeon, draw


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


class Renderer(object):
    def __init__(self, w, h):
        self.resolution = (w, h)
        self.screen     = pygame.display.set_mode((w, h), pygame.DOUBLEBUF | pygame.OPENGL | pygame.OPENGLBLIT)

        self.x = 0.0
        self.y = -1.0
        self.z = -5.0

    def ortho(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0.0, self.resolution[0], self.resolution[1], 0.0, -0.01, 10.0)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def perspective(self):
        self.aspect_ratio = self.resolution[0] / self.resolution[1]
                           
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, self.aspect_ratio, 0.1, 30.0)
        gl.glTranslatef(self.x, self.y, self.z)

        gl.glMatrixMode(gl.GL_TEXTURE)
        gl.glLoadIdentity()
        # @NOTE: invert y-coordinates, else textures are upside down
        gl.glScalef(1.0, -1.0, 1.0);
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()         
        gl.glEnable(gl.GL_DEPTH_TEST)

    def clear(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def update(self):
        pygame.display.flip()



# ---------------------------------------------------------------------

def build_dungeon_vertices(dungeon):
    neighbor_iteration = [(-1, 0, draw.WestWallTile), (1, 0, draw.EastWallTile), (0, 1, draw.SouthWallTile), (0, -1, draw.NorthWallTile)]
    white = (1.0, 1.0, 1.0)
    black = (0.0, 0.0, 0.0)
    yellow = (1.0, 1.0, 0.0)
    
    tiles = list()
    for y in range(dungeon.size[1]):
        for x in range(dungeon.size[0]):
            c = dungeon[(x, y)]
            if c.isWall():
                continue
            
            if c.isFloor():
                t = draw.FloorTile(3.0, 2.0)
                t.moveTo(x * 3.0, 0.0, y * 3.0)
                t.texture = tileset 
                t.clip(0.0, 0.0, 1.0, 0.5)
                tiles.append(t)

            # place walls around floor/void    
            for neighbor in neighbor_iteration:
                newx = x + neighbor[0]
                newy = y + neighbor[1]
                c2 = dungeon[(newx, newy)]
                if c2 is not None and not c2.isWall():
                    continue
                t = neighbor[2](3.0, 2.0)
                t.moveTo(x * 3.0, 0.0, y * 3.0)
                t.texture = tileset      
                t.colorize(yellow, yellow, white, white)
                t.clip(0.0, 0.5, 1.0, 0.5)
                tiles.append(t)

            if c.isVoid():
                # place lower walls in void's pit
                for neighbor in neighbor_iteration:
                    newx = x + neighbor[0]
                    newy = y + neighbor[1]
                    # TODO: get --> None
                    c2 = dungeon[(newx, newy)]
                    if c2 is not None and c2.isVoid():
                        continue
                    t = neighbor[2](3.0, 2.0)
                    t.moveTo(x * 3.0, -2.0, y * 3.0)
                    t.texture = tileset
                    t.colorize(white, white, black, black)  
                    t.clip(0.0, 0.5, 1.0, 0.5)
                    tiles.append(t)
    return tiles            

if __name__ == '__main__':
    pygame.init()
    renderer = Renderer(640, 480) 
    running  = True

    fpsclock = pygame.time.Clock()

    tileset = draw.Texture()
    tileset.loadFromFile('tileset.png')

    heart = draw.Texture()
    heart.loadFromFile('heart.png')
    
    #minimap = createMinimap(tileset, d, 16)

    hud = draw.Sprite2D(32, 32)
    hud.moveTo(16, 16)
    hud.texture = heart
    
    # demo terrain
    d = dungeon.Dungeon()
    d.loadFromFile('demo.txt')
    tiles = build_dungeon_vertices(d)

    next_fps_update = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_w]:
            renderer.z += 0.1
        if key_input[pygame.K_s]:
            renderer.z -= 0.1
        if key_input[pygame.K_a]:
            renderer.x += 0.1
        if key_input[pygame.K_d]:
            renderer.x -= 0.1
        if key_input[pygame.K_q]:
            renderer.y -= 0.1
        if key_input[pygame.K_e]:
            renderer.y += 0.1

        renderer.clear()
        
        renderer.ortho()
        hud.render()

        renderer.perspective()
        for t in tiles:
            t.render()

        #screen.blit(minimap, (50, 50))
        renderer.update()
        fpsclock.tick(60)

        since = pygame.time.get_ticks()
        if since > next_fps_update:
            fps = 'pyCrawler prototype - {0} FPS'.format(int(fpsclock.get_fps()))
            pygame.display.set_caption(fps)
            next_fps_update = since + 1000

    pygame.quit()
