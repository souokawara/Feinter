'''
GAME ENGINE
'''
import torch
import scipy as sp
import torchquad as quad
import pygame as game
from sympy import *
from sympy import I,pi,E
import Assets as assets
'''
PHYSICS

MTS Unit System

the density of the objects will be abstracted to the average
all the physical objects are ideally solid
'''

# managing the physical environment as the whole in the assets array
class Physics:
    def __init__(self):
        self.t = torch.tensor([0.0]) # time
        self.fps = torch.tensor([]) # fps for the Graphic class
        self.dt = torch.tensor(self.t/self.fps) # the effective differential physical time in the game
        self.g = torch.tensor([9.8]) # gravity constant
        self.r = torch.tensor([0.2]) # the air resistance
        self.assets_id = torch.tensor([]) # assets handler

    def register(self, name):
        self.id = id(self)
        self.name = name
        self.assets_id = torch.add(self.assets_id,self.id)

        self.x = torch.zeros([3,1]) # positions
        self.f = torch.zeros([3,1]) # kinetical forces
        self.a = torch.zeros([3,1]) # kinetical accelerations
        self.c = torch.tensor([]) # the center of gravity
        self.xi = torch.tensor([3,1]) # the angular accelerations on the center of gravity
    
    def def_attr(self, weight, length, pos, phi, bounce, friction):
        self.w = torch.tensor([weight]) # the weight
        self.length = torch.tensor(length) # size in 3d
        self.d = torch.tensor([self.w/self.length[0]*self.length*[1]*self.length[2]]) # the density on the object
        self.pos = torch.tensor(pos) # the position in 3d
        self.phi = torch.tensor(phi) # the angles in 3d (xy, yz, zx)
        self.bounce = torch.tensor([bounce]) # bounce rate, 0 <= bounce <=1
        self.friction = torch.tensor([frinction]) # the friction rate, 0 <= friction <= 1 

    def acc_vec(self, pos, f): # pos is the hitting point of the accelerated object

        # the impulse of the forces per frame
        # dt = t(sec)/fps
        # impulse = int_{t_1}^{t_2} f_n dt + f_{t_1}
        # f_n = 
        return 0
         
    def acc_ang(self, flucrum, f): # defining the angular accelerations for the flucrum
        # return the single momentum for the gravity central

        return 0
    def leverage(self,stress,flucrum,f): # defining the momentum of the object
        # return the sum of the momentum around the gravity central
        # define the 3d line from the stress to the flucrum
        # define the antipodal point on the object
        # define the friction on the hitting point of the object
        # define the collision angles of each surface
        ap  = (flucrum - stress) * f
        
    def collide(self): # judging the collision in the assets per frame
        # judge if collison emerges
        # define the frictions and the collisions to return to the leverage
        return 0

    def air_friction(self):
        # define the air friction on the obejcts

        return 0

    # the core procedure
    def motion(self):
        self.acc_vec()
        self.acc_ang()
        self.collide()
        
test = Physics()
test.register("ball")
print(test.id)

'''
GRAPHICS
'''
# define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

class Graphics:
    def __init__(self):
        # the window settings
        self.size = (650, 1000)
        self.caption = "Beta Graphic"
        self.screen = game.display.set_mode(size)
        self.game.display.set_caption(caption)
        self.display = game.display

        # the fps
        self.fps = game.time.Clock()
        self.fps = 60

        # close flag
        self.close = False

    def update(self):
        self.display.flip()
        return 0
        
'''
PHYSICS INTERFACE TO ASSETS
'''


'''
MAIN LOOP
'''
def main():
    game.init()
    print("test")
    game.quit()
    return 0

if __name__ == '__main__':
    main()
