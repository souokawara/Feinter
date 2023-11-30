'''
THE FEINT PLAYER MODEL

the pong simulation where bilateral players learn each other's learning process itself by the movement of the ball and the opponent; given each player can survey the trajections of the ball and the other player. each could have the incentive to conceal the learning processes and the differential traces to be surveyed by the other player, only in the movement in the pong game.

'''

'''
LIBRALIES
'''

import numpy as np
import torch
# import sklearn as sk
# import torchquad

# this program will be the outlet model of softgraph.py
import softgraph


'''
THE TENNIS COURT
'''

class Court:
    def __init__(self, if_solo, width, height, friction, fence_height, weight_cols, weight_ars):
        # time dimention
        self.t = 0.0
        # previous time
        self.previous = 0.0

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
        self.power = 0.03 # the acceleraation of the swing
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
        # debugger
        # print("Ball.f", Ball.f, "stamina", self.stamina, "Ball.weight", Ball.weight,
        #        "Player.weight", self.weight, "swing phi", self.phi,
        #        "Player.power", self.power)
    
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
        if (self.service_turn == self.name) and (self.t == 0) and (self.xyz == Ball.xyz):
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

    def get_body(self, weight, diameter, bounce):
        self.weight = weight
        self.diameter = diameter
        self.boucne = bounce

    def collide_wall(self, index):
        if index == 1:
            self.f[0] *= -1
        elif index == 2:
            self.f[1] *= -1
        elif index == 3:
            self.f[1] *= -1
        elif index == 4:
            self.f[2] *= -1
        else:
            pass
    
    def if_collide_fence(self, Court):
        if (self.f[0] >= 0) and (self.xyz[0] > Court.width / 2.0) and (self.xyz[2] < Court.fence_height):
            print("net miss!")
            return 1
        elif (self.f[0] < 0) and (self.xyz[0] < Court.width /2.0 ) and (self.xyz[2] < Court.fence_height):
            print("net miss!")
            return 1
        else:
            print("net pass")
            return 0

    def run(self, Court):
        self.xyz = torch.tensor(self.xyz) + self.f
        self.f[2] +=  -0.01 * Court.g
        self.resistance()

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

# embody the court
# (if_solo, width, height, friction, fence_height, weight_cols, weight_ars)
court = Court(True, 40.0, 20.0, 0.2, 0.3, 4, 4)

# embody the ball
ball = Ball(True, 40.0, 25.0, 0.2, 0.7, 4, 4)
# (weight, diameter, bounce)
ball.get_body(0.5, 0.2, 0.5)
court.ball = ball

# embody the player
# the only player who doesn't have theory of mind
court.alice = Player(True, 40.0, 25.0, 0.2, 0.7, 4, 4)
court.alice.name = "alice"
# (weight, width, height, stamina)
court.alice.get_body(50.0,1.0,1.0, 100.0)
court.alice.stamina = 100

# set Mind class on alice
alice_mind = Mind(court.alice)

# initialize the postion of the players and the ball
# maybe this could be in the constructor 
court.alice.xyz = [0, court.height/2, 0]
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
    # debugger
    print(court.previous)

    court.alice.play(court.ball, alice_mind)

    # time procedure
    court.t += 0.01

    # the ball movement
    # the function of court.t
    court.ball.run(court)

    # collision judgement
    court.ball.collide_wall(if_collide(court))

    # debugger 
    # print("court time\n", court.t)
    # print("ball.f\n", court.ball.f)
    print("ball.xyz\n",court.ball.xyz)
    print("ball.xyz\n",court.ball.xyz)

    if (court.previous < court.width/2.0) and (court.width/2.0 < court.ball.xyz[0]): 
        if(court.ball.if_collide_fence(court)):
            return 1
        else:
            return 0
    else:
        pass

    court.previous = court.ball.xyz[0]
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
        elif court.ball.xyz[1] < 0.0:
            print("collide!")
            return 3
        elif court.ball.xyz[2] < 0.0:
            return 4
        else:
            return 0
    else:
        pass


'''
MAIN LOOP
'''

def main(interbal, match_point, setmatch):
    print(court.alice.xyz)
    while True:
        x = game(court)
        if x == 1:
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
