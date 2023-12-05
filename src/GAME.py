'''
here will come the PyGame codes of the "Sally and Anne Enjoy! Tennis"
'''

import pygame as game
from pygame.locals import * 
import PINGPONG

'''
GRAPHIC ENGIGNE
'''

'''
FUNCTIONS
'''

'''
INITIALIZE
'''

'''
MAIN LOOP
'''

def main():
    game.init()
    screen = game.display.set_mode((640, 240))
    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    GRAY = (127, 127, 127)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    size = 640, 240
    width, height = size

    # ball = game.image.load("ball.png")
    # rect = ball.get_rect()
    speed = [2,2]

    while True:
        running = True
        background = BLACK
        while running:
            screen.fill(background)
            for event in game.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    print(event)
                    start = event.pos
                    size = 0, 0
                    drawing = True
                elif event.type == MOUSEBUTTONUP:
                    print(event)
                    end = event.pos
                    size = end[0] - start[0], end[1] - start[1]
                    drawing = False
                elif event.type == MOUSEMOTION and drawing:
                    end = event.pos
                    size = end[0] - start[0], end[1] - start[1]
            game.display.update()
            game.quit()
    return 0

if __name__ == '__main__':
    main()
