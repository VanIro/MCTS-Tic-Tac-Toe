
#MCTS
import copy
import math
import random


def game_result( game):
    winner=None
    for g in Node.GameChecks:
        g_line = [game[gi[0]][gi[1]] for gi in g]
        if all_equal(g_line): winner = g_line[0] if g_line[0] in Node.players else None
        if winner is not None: break
    return winner

def all_equal(A):
    for i in range(len(A)-1):
        if not A[i]==A[i+1]:
            return False
    return True

def get_childs(game):
    return [(i,j) for i in range(3) for j in range(3) if game[i][j] == 0]

def simulate(game, player_i):

    result=None
    while result is None:
        choices = get_childs(game)
        if len(choices)==0: 
            result=game_result(game)
            if result is None: break #this is a draw
        else:
            i,j = random.choice(choices)
            game[i][j] = player_i
            result = game_result(game)
            player_i = 1-player_i

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
    def lost(self):
        self.losses+=1
        # self.wins-=1

   

    def simulate(self):
        self.n_sims+=1
        result = simulate(copy.deepcopy(self.game), self.player_i)

        if result == Node.players[self.player_i]:
            self.won()
            return 1
        elif result == Node.players[1-self.player_i]:
            self.lost()
            return -1
        return 0

    def getUCB(self,t):
        if self.n_sims==0: return float('inf')
        return (self.wins-self.losses)/self.n_sims + self.c*(math.log(t)/self.n_sims)**.5
    
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
            max_val=-1
            for nd in childs:
                val = nd.getUCB(t)
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
        if len(childs)>0:
            child = random.choice(childs2)
            result = child.simulate()
        else:
            result = 0 #draw

        #BackPropagation
        parent = child.parent
        while parent is not None:
            result = -result # win for child is loss for parent and so on...
            match result:
                case 1:
                    parent.won()
                case -1:
                    parent.lost()
            parent.n_sims+=1
            parent = parent.parent

        
        t+=1
    #get UCB position
    priority_childs = sorted(root.childs,key=lambda nd: nd.n_sims,reverse=True)
    print(root.childs)
    return priority_childs[0]


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