'''
THE FEINT PLAYER MODEL

the pong simulation where bilateral players learn each other's learning process itself by the movement of the ball and the opponent; given each player can survey the trajections of the ball and the other player. each could have the incentive to conceal the learning processes and the differential traces to be surveyed by the other player, only in the movement in the pong game.

'''

'''
LIBRALIES
'''

import numpy as np
import torch
import torchquad as quad
import pygame as game

# from sklearn

# this program will be the outlet model of softgraph.py
import softgraph


'''
THE TENNIS COURT
'''

class Court:
    def __init__(self, if_solo, width, height, friction, fence_height, weight_cols, weight_ars):
        # time dimention
        self.t = 0.0

        # the gravity
        self.g = 9.8

        # the physical attributes
        self.if_solo = if_solo # when True for the solo learning
        self.width = width
        self.height = height
        self.friction = friction
        self.fence_height = fence_height
        self.border = [height,0,width,0]
        # for the solo learning
        self.wall = self.if_solo

        # the ball
        self.ball = None
 
        # the players
        self.alice = None

        # service turn
        self.service_turn = "alice"

        # the score board
        self.match = torch.zeros((1,2))
              
        # the judgement of the game
        self.judge = 0
        
        # solo learning mode
        if self.if_solo == True:
            self.set_wall()
        else:
            pass

    # to set wall for the solo learning
    def set_wall(self):
        return 0
    

'''
TENNIS PLAYERS

the moving bord as a racket which is to accelerated by some god hand
to be serious as a game each player has some physical limit for the tactics
'''

class Player(Court):
    def __init__(self, if_solo, width, height, friction, fence_height, weight_ars, weight_cols):

        # refering Court class
        super().__init__(if_solo, width, height, friction, fence_height, weight_ars, weight_cols)

        # (x,y,z) as physics
        self.xyz = torch.zeros((1,3))
        # differential force on (x,y,z)/t
        self.f = torch.zeros((1,3))

        # physical attributes of the player
        self.weight = 0.0
        self.height = 0.0
        self.width = 0.0
        self.stamina = 0.0

        # name
        self.name = None
        
        # w1 for the weight matrix for the self technique
        self.w1 = torch.rand((weight_ars, weight_cols))
        
        # w2 for the weight matrix for the other's intentions
        self.w2 = torch.rand((weight_ars, weight_cols))
        
        # the attributes for the swinging
        # the opponent can only survey and learn the swinging by its result as the trajectory of the ball
        self.phi = 0 # the angular of the swing
        self.power = 0.003 # the acceleraation of the swing
        self.axis = [self.width/2, self.height/2] # the axis of the angular movement which is movable
        
        # the coupon to declare the time break
        self.time = 2

    def get_body(self, weight, height, width, stamina):
        self.weight = weight
        self.height = height
        self.width = width
    
    # to decide the angular accelaration from the player as the board on the court by the axis
    def swing(self,phi, Ball):
        self.stamina -= 0.1 * self.weight
        self.phi = phi
        self.power *= self.weight
        self.axis

        # hitting the ball
        Ball.f += torch.div(torch.tensor([self.power * torch.cos(self.phi),
                self.power * torch.sin(self.phi), 0]), Ball.weight)
        print("hit!")
   
    # only for the serve swing
    def toss(self, Ball):
        self.stamina -= 0.1
        Ball.f += torch.div(torch.tensor([0,0,self.power]) , Ball.weight)
    
    # moving in xyz space by the stamina
    def run(self, phi, d):
        self.stamina -= 0.1 * self.weight
        # F
        self.f += torch.tensor([d * torch.cos(phi), d * torch.sin(phi), 0])
        # a = m/F
        self.xyz += torch.div(self.a , self.weight) 
    
    # recovery of the stamina by not moving differentially
    def recover(self):
        # will be differentially later on
        if self.f == 0 :
            self.stamina += torch.tensor([0.1])
        else:
            pass
    
    # declaring the time break as the strategy
    def time(self, Mind):
        return 0
    
    # output on the court play    
    def play(self, Ball, Mind):
        if (self.service_turn == self.name) and (self.t == 0) and torch.equal(self.xyz, Ball.xyz):
            # the serve
            self.toss(Ball)
            print("tossed")

        elif (self.t != 0) and (self.xyz != Ball.xyz):
            # learning timely when the ball is out there...
            Mind.learn()
            print("minding...")

        elif (self.xyz[0] == Ball.xyz[0]) and (self.xyz[1] == Ball.xyz[1]) and (self.xyz[2] > Ball.xyz[2]):
            # when the tossed ball has come on
            self.swing(torch.tensor(np.pi*0.25), Ball) # improvisional constants
            print("swung!")
        else:
            pass
    
    # for the interbal or the time declartion
    def sit(self, Mind, interbal):
        self.recover()
    
    # collision to the fence
    def collide_fence(self, Court):
        if (self.xyz == self.wall) :
            self.f *= torch.tensor([-1,0,0])
        elif (self.xyz == self.wall):
            self.f *= torch.tensor([0,-1,0])
        else:
            pass

'''
THE BALL
'''

class Ball(Court):
    def __init__(self, if_solo, width, height, friction, fence_height, weight_ars, weight_cols):
        # refering Court class
        super().__init__(if_solo, width, height, friction, fence_height, weight_ars, weight_cols)
        self.xyz = torch.tensor([0.0,0.0,0.0])
        self.weight = 0.0
        self.diameter = 0.0
        self.bounce = 0.0
        self.f = torch.tensor([0.0,0.0,0.0])
        self.collide = False

    def get_body(self, weight, diameter, bounce):
        self.weight = weight
        self.diameter = diameter
        self.boucne = bounce

    '''
    STUCK!!!

    somehow the ball throughs the wall
    '''
    def collide_wall(self, index):
        if index == 1:
            print("!")
            self.f[0] *= -1
            self.collide = True
        elif index == 2:
            print("!")
            self.f[1] *= -1
            self.collide = True
        elif index == 3:
            print("!")
            self.f[0] *= -1
            self.collide = True
        else:
            pass

    def bound_ground(self):
        self.f[2] *= -1

    def if_collide_fence(self, Court):
        return self.xyz[0] <= Court.height/2.0 <= self.xyz[0] +self.diameter and Court.fence_height >= self.xyz[1] + self.diameter

    def run(self, Court):
        self.xyz = torch.add(self.xyz, self.f)
        self.f[2] +=  -0.01 * Court.g
        self.resistance()
        
        # collide flag management
        if if_in(Court):
            self.collide = False
        else:
            pass

    # the ball would reduce its acceleration by the resistance in the air
    def resistance(self):
        self.f *= 0.98  # improvisional       
        

'''
MIND

the main engine to interpret the other player's learning process
and the learning engine itself, where the player infers the other's mind
according to the own learning process.
'''

class Mind(Player, Court):
    def __init__(self,Player):
        self.name = Player.name
        self.w1 = Player.w1
        self.w2 = Player.w2
    
    # for the others
    def survey(self, Player, Court):
        Player.xyz #the opponent
        Player.f
        Court.ball.xyz
        Court.ball.f

    
    # for the self
    # for the first beta, the orthodox DL model would be deployed
    # on this function on the test player Alice
    def learn(self, Player, Court):
        Player.xyz # the self
        Player.f
        Court.ball.xyz
        Court.ball.f
        
        # the beta goal of the solo-learning Alice model
        # is just to avoid the net-miss in 3d space



'''
INITIALIZE

this space seems too ugly for now...
'''

# measured in MKS

# embody the court
# (if_solo, width, height, friction, fence_height, weight_cols, weight_ars)
court = Court(True, 8.23, 23.77, 0.1, 0.914, 4, 4)

# embody the ball
ball = Ball(True, 8.23, 23.77, 0.1, 0.914 , 4, 4)
# (weight, diameter, bounce)
ball.get_body(0.0567, 0.0654, 0.85)
court.ball = ball

# embody the player
# the only player who doesn't have theory of mind
court.alice = Player(True, 8.23, 23.77, 0.1, 0.914 , 4, 4)
court.alice.name = "alice"
# (weight, width, height, stamina)
court.alice.get_body(54.7, 1.61, 1.61, 100.0)

# set Mind class on alice
alice_mind = Mind(court.alice)

# initialize the postion of the players and the ball
# maybe this could be in the constructor 
court.alice.xyz = torch.tensor([0, court.width/2.0, 0])
if court.service_turn == court.alice.name:
    court.ball.xyz = court.alice.xyz
    court.ball.xyz[2] += court.alice.height
else:
    print("something is wrong")


'''
GAME PARAMETERS
'''

# the break duration
interbal = 100

# the match point
match_point = 5

# the set match
set_match = 10


'''
FUNCTIONS

for the main loop
'''

def game(court):
    # alice to play the game
    court.alice.play(court.ball, alice_mind)

    # time procedure
    court.t += 0.01

    # the ball movement
    court.ball.run(court)

    # landing judgement
    if if_land(court):
        court.ball.bound_ground()
    else:
        pass

    # collision judgement
    if not if_in(court) and court.ball.collide == False:
        court.ball.collide_wall(if_collide(court))
    elif not if_in(court) and court.ball.collide == True:
        pass
    else:
        court.ball.collide = False
        court.ball.collide_wall(if_collide(court))

    # to the fence
    if court.ball.if_collide_fence(court):
        return 1
    else:
        pass
    
    print("ball.xyz\n",court.ball.xyz)
def match(match_point, court):
    game(court)

    return court.judge

def set_match(set_match,match_point):
    match(match_point)
    
    return court.judge

def interbal(interbal):
    court.alice.sit(alice, interbal)

# judging the collisions on the court
def if_collide(court):
    if court.wall:
        if court.ball.xyz[0] > court.width:
            print("collide!")
            return 1
        elif court.ball.xyz[1] > court.height:
            print("collide!")
            return 2
        elif court.ball.xyz[0] < 0.0:
            print("collide!")
            return 3
        elif court.ball.xyz[1] < 0.0:
            print("ball pass! game over!")
            return 5
        else:
            return 0
    else:
        pass

# judging the in-out of the ball
def if_in(court):
    return 0 <= court.ball.xyz[0] <= court.width and 0 <= court.ball.xyz[1] <= court.height

# judgin the landing of the ball
def if_land(court):
    return 0.0 >= court.ball.xyz[2]
'''
MAIN LOOP
'''

def main(interbal, match_point, setmatch):
    for i in range(120):
        x = game(court)
        if x == 1:
            print("game over!")
            break
        else:
            continue
    # the game point
    return court.judge


'''
THE DATABASE

to store the save data 
'''
class Data:
    pass


if __name__ =='__main__':
    main(interbal, match_point, set_match)
