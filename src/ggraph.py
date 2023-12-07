import numpy as np
import torch
import matplotlib.pyplot as plt

""" CLASS """

# to learn the market to modify the rate per a*t to maximize the gross profit
class CentralBank:

    def __init__(self, r):
        self.r = r

    def up(self): 
        return 0
    def down(self):
        return 0
    def search(self):
        return 0

# to capitalize indivisual profit unless the crush of the market
class Bank:
    def __init__(self, n):
        self.id = n
        self.borrows = 0
        self.lends = 0
        self.balance = self.lends - self.borrows
        self.borrower_interests = np.array(n,[])
        self.lender_interests = np.array(n,[])
        self.available
        # for deep learning
        self.weight = 0

    # the beneficial function
    def rate(self):
        indices = self.available - 1
        
        ''' UNDER CONSTRUCTION '''
        minimum_borrow_interest = np.min(np.take(self.borrower_interests, indices))
        maximum_lend_interest = np.max(np.take(self.lender_interests, indices))
        ''' UNDER CONSTRUCTION '''
        
        # making decision by the weight
        # this formula is almost random for now
        if maximum_lend_interest >= (self.weight + minimum_borrow_interest)/2:
            # return id to lend
            return np.where(self.lender_interests == maximum_lend_interest)
        else:
            # return id to borrow
            return np.where(self.borrower_interests == minimum_borrow_interest)
    
    # available trades
    def available(self, adjacency):
        available = np.array([]) 
        count = 0
        for i in adjacency[self.id-1]:
            if i == 1:
                available = np.append(available, count)
            count += 1
        return available

# to negotiate correctively to fit into the coming central bank strategy
class Market:
    def __init__(self, n, r):
        # set the adjacency matrix at random
        self.adjacency = np.random.randint(0,2,(n,n))
        self.banks = []
        self.cb = CentralBank(r)
        
        # initialize the banks
        while n:
            bank = Bank(n)
            self.banks.append(bank)
            n -= 1
            
        # distribute the banks the interests, the initial balances and weights
        for bank in self.banks:
            bank.lender_interests = np.random.rand(n)
            bank.borrower_interests = np.random.rand(n)
            bank.weight = np.random.rand()
            bank.borrows = np.random.randint(10,1000)
            bank.lends = np.random.randint(10,1000)
            
        # suming up the initial gross
        borrows = np.array([bank.borrows for bank in self.banks])
        lends = np.array([bank.lends for bank in self.banks])
        # gross = lends - borrows
        self.gross = np.sum(lends) - np.sum(borrows)
    
    def sum_gross(self,balance):
        return 0
    
    def set_lend(self, server_id, reciever_id, amount):
        self.banks[server_id].balance -= amount
        self.banks[server_id].lends += amount
        self.banks[reciever_id].borrows += amount
    
    def set_borrow(self, server_id, reciever_id, amount):
        self.banks[server_id].borrows += amount
        self.banks[reciever_id].lends += amount
        self.banks[reciever_id].balance -= amount
    
    # multiply the interest rates both borrows and lends per time
    def get_interests(self):
        for bank in self.banks:
            for borrow in bank.borrows:
                borrow *= bank.borrower_interests[np.where(bank.borrows == borrow)]
                
        for bank in self.banks:
            for lend in bank.lends:
                lend *= bank.lenders_interests[np.where(bank.lends == lend)]
    
    # relating the benefits via Bank.rate()
    def set_relation(self, server_id, reciever_id):
        # if the befits concent
        if (self.banks[server_id].rate() == reciever_id) and (self.banks[reciever_id].rate() == server_id):
            # the amount to lend
            return self.banks[server_id].balance * self.banks[server_id].weight
        else:
            return 0 
        

""" INITIALIZE """

# 10 banks on the graph, 2.0 as the initial rate
market = Market(10,2.0)

# the time duration
t = 100

# the periodical rating
a = 5

# available trades initializing currently
for bank in market.banks:
        bank.available = bank.available(market.adjacency)

""" MAIN """

def main(a,t):
    """
    while t:
        # the negotiation round per t
        while bank in market.banks:
            for available_id in bank.available:
                amount = market.set_relation(bank.id, available_id)
                if amount != 0:
                    # inprovisional part
                    market.set_lend(bank.id,available_id, amount)
                    market.set_borrow(available_id, bank.id, amount)
                else:
                    pass
        
        # the date to profit
        market.get_interests()
        print(market.gross)
        t -= 1
    """
    # print(torch.cuda.is_available())
    return 0
   
    
    
if __name__ == '__main__':
    main(a,t)

