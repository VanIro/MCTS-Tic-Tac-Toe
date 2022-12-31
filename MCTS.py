#MCTS
import copy
import math
import random

#returns -1 for draw, index of winner in Node.players if someone has won, else None 
def game_result( game):
    winner=None
    no_draw = False
    for g in Node.GameChecks:
        g_line = [game[gi[0]][gi[1]] for gi in g]
        if all_equal(g_line): winner = g_line[0] if g_line[0] in Node.players else None

        p1, p2 = Node.players
        if not (p1 in g_line and p2 in g_line):
            no_draw = True

        if winner is not None: break
    
    if not no_draw: return -1
    elif winner is not None: return Node.players.index(winner)

def all_equal(A):
    for i in range(len(A)-1):
        if not A[i]==A[i+1]:
            return False
    return True

def get_childs(game):
    return [(i,j) for i in range(3) for j in range(3) if game[i][j] == 0]

def print_board(game):
    for r,row in enumerate(game):
        for cell in row:
            print(cell, end="\t")
        print("/*\\\t",end='')
        for i in range(3):
            print(i+3*r + 1 if row[i]==0 else 'X', end="\t")
        print('')
    print("="*50)

def simulate(game, player_i):

    result=None
    while result is None:
        choices = get_childs(game)
        if len(choices)==0: 
            result=game_result(game)
        else:
            i,j = random.choice(choices)
            game[i][j] = Node.players[player_i]
            result = game_result(game)
            player_i = 1-player_i
    
    # print("Simulating...")
    # print_board(game)
    # print("Result: ",result)
    # print("<"*50)

    return result


class Node:
    c=2**.5
    players = [1,2]
    GameChecks = [[(i,j)for j in range(3)] for i in range(3)]+\
        [[(j,i)for j in range(3)] for i in range(3)]+\
        [[(i,i) for i in range(3)]]+[[(i,2-i) for i in range(3)]]

    def __init__(self,game,player_i,pos=None,parent=None) -> None:
        self.wins=0
        self.losses=0
        self.draws=0
        self.n_sims=0
        self.game = game#copy.deepcopy(game)
        self.parent = parent
        self.pos = pos
        self.childs=[]
        self.player_i = player_i

    def __repr__(self):
        return "Node< "+str(self.pos[0]*3+self.pos[1]+1)+"> ["+str(self.wins)+'/'+str(self.n_sims)+' ]'
  
    
    
    def get_childs(self):
        return get_childs(self.game)

    
    def game_result(self):
        return game_result(self.game)

    def won(self):
        self.wins+=1
    def drawn(self):
        self.draws+=1
    def lost(self):
        self.losses+=1
        # self.wins-=1

   
    #returns 1 for win, -1 for loss and 0 for draw
    def simulate(self):
        # self.n_sims+=1
        result = simulate(copy.deepcopy(self.game), self.player_i)

        if result == self.player_i:
            # self.won()
            return 1
        elif result == 1-self.player_i:
            # self.lost()
            return -1
        return 0

    def get_sim_score(self):
        return self.wins

    def getUCB(self,t):
        if self.n_sims==0: return float('inf')
        kw=1
        kd=0
        kl=0
        exploit_score =  self.wins/self.n_sims#(kw*self.wins + kd*self.draws -kl*self.losses)/(self.n_sims + (kw-1)*self.wins + (kd)*self.draws)
        return exploit_score + self.c*(math.log(t)/self.n_sims)**.5
    
    def expand(self):
        childs = self.get_childs()
        pre_childs = [child.pos for child in self.childs] # positions of existing childs
        childs = [child for child in childs if child not in pre_childs]
        # if len(self.childs)>0: return False
        next_player_i = 1-self.player_i
        # print('expand : ',self.get_childs())
        for i,j in self.get_childs():
            game = copy.deepcopy(self.game)
            game[i][j]=self.players[self.player_i]
            nd = Node(game,next_player_i,(i,j),self)
            self.childs.append(nd)
        return True




def MCTS_sim(root:Node,NT:int, Tbeg:int):
    t=Tbeg
    Tmax = Tbeg + NT
    while t<Tmax:
        #selection
        node = root
        while True:
            childs = node.childs
            if len(childs)==0:
                break
            max_childs=[]
            max_val=childs[0].getUCB(node.n_sims)
            for nd in childs:
                val = nd.getUCB(node.n_sims)
                if val>max_val:
                    max_val=val
                    max_childs=[nd]
                elif val==max_val:
                    max_childs.append(nd)
            # print("selection:")
            # print(max_val,max_childs)
            node = random.choice(max_childs)
        
        #expansion
        node.expand()

        #simulation
        childs2 = node.childs
        if len(childs2)>0:
            child = random.choice(childs2)
            # print(child.pos[0]*3+child.pos[1]+1)
            result = child.simulate()
        else:
            result = 0 #draw
            child = node

        #BackPropagation
        parent = child
        while parent is not None:
            match result:
                case 1:
                    parent.won()
                case -1:
                    parent.lost()
                case 0:
                    parent.drawn()
            parent.n_sims+=1
            parent = parent.parent
            result = -result # win for child is loss for parent and so on...

        
        t+=1
    #get UCB position
    priority_childs = sorted(root.childs,key=lambda nd: nd.get_sim_score(),reverse=False)
    if len(priority_childs)>0:
        max_wins = priority_childs[0].get_sim_score()
        priority_childs = [child for child in priority_childs if child.get_sim_score()==max_wins]
    print(root.childs)
    return priority_childs


# def print_tree(root:Node):
#     node = root
#     while True:
#         childs = node.childs
#         if len(childs)==0:
#             break
#         max_childs=[]
#         max_val=-1
#         for nd in childs:
#             val = nd.getUCB(t)
#             if val>max_val:
#                 max_childs=[nd]
#             elif val==max_val:
#                 max_childs.append(nd)
#         node = random.choice(max_childs)