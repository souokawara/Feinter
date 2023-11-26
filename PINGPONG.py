'''
THE FEINT PLAYER MODEL

the pong simulation where bilateral players learn each other's learning process itself by the movement of the ball and the opponent; given each player can survey the trajections of the ball and the other player. each could have the incentive to conceal the learning processes and the differential traces to be surveyed by the other player, only in the movement in the pong game.

the learning process of the each player should be strictly separated, only the view on the arena may be fully learnable for each; especially the differential velocity of the other player is highly remarkable, including the feint technique.

'''
import torch
import sklearn as sk

# this program will be the outlet model of softgraph.py
from . import softgraph


# The Tennis Court
class Court:
    def __init__(self, width, height, friction, fence_height, weight_cols, weight_ars):
        # the physical attributes
        self.width = width
        self.height = height
        self.friction = friction
        self.fence_height = fence_height
        self.border = [height,0,width,0]
        
        # the score board
        self.match = torch.zeros((1,2))
        
        # the players
        self.sally = Player(weight_ars,weight_cols)
        self.anne = Player(weight_ars,weight_cols)
        self.sally.name = "sally"
        self.anne.name = "anne"
        
        # the ball
        self.ball = Ball()
        
        # the judgement of the game
        # when sally wins to 1, if else stays 0
        self.judge = 0

# Tennis Players
# the moving bord as a racket which is to accelerated by some god hand
# to be serious as a game each player has some physical limit for the tactics
class Player(Court):
    def __init__(self, weight_ars, weight_cols):
        # (x,y,z) as physics
        self.xyz = torch.zeros((1,3))
        self.a = torch.zeros((1,3))
        
        # physical attributes
        self.weight = 0
        self.height = 0
        self.width = 0
        self.stamina = 0

        # name
        self.name = None
        
        # w for the weight matrix for the self tequenique
        self.w1 = torch.rand((weight_ars, weight_cols))
        
        # w for the weight matrix for the other's intentions
        self.w2 = torch.rand((weight_ars, weight_cols))
        
        # the attributes for the swinging
        # the opponent can only survey and learn the swinging by its result as the trajectory of the ball
        self.phi = 0 # the angular of the swing
        self.power = 0 # the acceleraation of the swing
        self.axis = [self.width/2, self.height/2] # the axis of the angular movement which is movable
        
        # the coupon to declare the time break
        self.time = 2
    
    def get_body(self, weight, height, width, stamina):
        self.weight = weight
        self.height = height
        self.width = width
    
    # to decide the angular accelaration from the player as the circle on the court
    def swing(self,Court):
        self.stamina
        self.phi
        self.power
        self.axis
        return 0
    
    # only for the serve swing
    def toss(self, Court):
        self.stamina
        return 0
    
    # moving in xyz space by the stamina
    def run(self, Court):
        self.stamina
        self.xyz
        self.a
        return 0
    
    # recovery of the stamina by not moving differentially
    def recover(self, Court):
        self.stamina
        self.a
        return 0
    
    # declaring the time break as the strategy
    def time(self, Court):
        return 0
    
    # output on the court play    
    def play(self, Mind):
        return 0
    
    # for the interbal
    def sit(self, Mind, interbal):
        return 0
    
    # collision to the fence
    def collide(self, Court):
        return 0

    
# The Ball
class Ball(Court):
    def __init__(self):
        self.xyz = torch.zeros((1,3))
        self.weight = 0
        self.diameter = 0
        self.bounce = 0
        self.a = torch.zeros((1,3))

    def get_body(self, weight, diameter, bounce):
        self.weight = weight
        self.diameter = diameter
        self.boucne = bounce
        
# The Learning Process
class Mind(Player, Court):
    def __init__(self,Player):
        self.name = Player.name
        self.w1 = Player.w1
        self.w2 = Player.w2
    
    # for the others
    def survey(self, Player, Court):
        Player.xyz #the opponent
        Player.a
        Court.ball.xyz
        Court.ball.a

    
    # for the self
    def learn(self, Player, Court):
        Player.xyz # the self
        Player.a
        Court.ball.xyz
        Court.ball.a


'''
INITIALIZE
'''
# (width, height, friction, fence_height, weight_cols, weight_ars)
court = Court(40.0, 25.0, 0.2, 0.7, 4, 4)

# embody the ball
# (weight, diameter, bounce)
court.ball.get_body(0.5, 0.2, 0.5)

# embody the players
# (weight, height, width, stamina)
court.sally.get_body(50.0,1.0,1.0, 100.0)
court.anne.get_body(50.0,1.0,1.0, 100.0)

sally = Mind(court.sally)
anne = Mind(court.anne)

'''
MAIN VARIABLES
'''
# the break duration
interbal = 100

# the match point
match_point = 5

# the set match
set_match = 10


'''
FUNCTIONS
'''

def game(court):
    court.sally.play()
    court.anne.play()

def match(match_point, court):
    game(court)

    return court.judge

def set_match(set_match,match_point):
    match(match_point)
    
    return court.judge

def interbal(interbal):
    court.sally.sit(sally, interbal)
    court.anne.sit(anne, interbal)



'''
MAIN
'''
def main(interbal, match_point,setmatch):
    while True:
        try:
            set_match(set_match, match_point)
        except:
            break
    
    # the game point
    return court.judge


'''
THE DATABASE
'''
class Data:
    pass


if __name__ =='__main__':
    main(interbal, match_point, set_match)