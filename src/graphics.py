'''
GAME ENGINE
'''

import os
import pygame as game
import pygame.draw as draw
import pygame.camera
import Assets as assets
import physics

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

current_directory = os.getcwd()
video = os.path.join(current_directory,"video")


'''
''
GRAPHICS
'''
# define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

class Graphics:
    def __init__(self,game):
        # the window settings
        self.game = game
        self.size = (650, 1000)
        self.game.caption = "Beta Graphic"
        self.screen = game.display.set_mode(self.size)

        # the fps
        self.fps = game.time.Clock()
        self.fps = 60

        # close flag
        self.close = False

    # create cube
    def make_cube(self, pos_x, pos_y, width, height):
        self.game.draw.rect(self.screen, WHITE, game.Rect(pos_x, pos_y, width, height))

    
    def update(self):
        self.game.display.flip()
        return 0
        
'''
PHYSICS INTERFACE TO ASSETS
'''


'''
MAIN LOOP
'''
def main():
    game.init()
    game.camera.init()
    graph = Graphics(game)
    while True:
        graph.screen.blit(image, (0,0))
        graph.update()
    graph.game.quit()
    return 0

if __name__ == '__main__':
    main()
