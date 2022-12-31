#MCTS
import copy
import math
import random

from utils import game_result,get_childs
from game import GameSettings

def simulate(game, player_i):
    # print("Simulating for player",GameSettings[player_i],"...")
    result=None
    while result is None:
        choices = get_childs(game)
        if len(choices)==0: 
            result=game_result(game)
        else:
            i,j = random.choice(choices)
            game[i][j] = GameSettings.players[player_i]
            result = game_result(game)
            player_i = 1-player_i
    
    # print_board(game)
    # print("Result: ",end='')
    # if result==-1: print("Draw")
    # else: print("Player ",GameSettings[result]," wins.")
    # print("<"*50)

    return result


class Node:
    c=2**.5
    def __init__(self,game,player_i,pos=None,parent=None) -> None:
        self.wins=0
        self.losses=0
        self.draws=0
        self.n_sims=0
        self.game = game
        self.parent = parent
        self.pos = pos
        self.childs=[]
        self.player_i = player_i

    def __repr__(self):
        return f"Node<{self.pos[0]*3+self.pos[1]+1}/{9-len(self.get_childs())}>({GameSettings[self.player_i]}) [{self.wins}/{self.n_sims}]"
  
    
    
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

   
    #returns 1 for win, -1 for loss and 0 for draw
    def simulate(self):
        result = simulate(copy.deepcopy(self.game), self.player_i)
        if result == self.player_i:
            return 1
        elif result == 1-self.player_i:
            return -1
        return 0

    #used this function to get self.wins indirectly just so that I could change it if required | didn't get required though
    def get_sim_score(self):
        return self.wins

    def getUCB(self,t):
        if self.n_sims==0: return float('inf')
        exploit_score =  self.wins/self.n_sims
        return exploit_score + self.c*(math.log(t)/self.n_sims)**.5
    
    def expand(self):
        childs = self.get_childs()
        pre_childs = [child.pos for child in self.childs] # positions of existing childs
        childs = [child for child in childs if child not in pre_childs]
        next_player_i = 1-self.player_i        
        for i,j in self.get_childs():
            game = copy.deepcopy(self.game)
            game[i][j]=GameSettings.players[self.player_i]
            nd = Node(game,next_player_i,(i,j),self)
            self.childs.append(nd)
        return True


def MCTS_sim(root:Node,n_iters:int):
    t=0
    root.expand()
    while t<n_iters:
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
            # print("selection:",end='')
            # print(max_val,max_childs)
            node = random.choice(max_childs)
        
        #expansion
        #this extra check was "required" so that all no unsimulated nodes would be 
        #expanded, which increases the breadth of search region
        if node.n_sims>0:
            node.expand()
        else:
            child = node

        #simulation
        childs2 = node.childs
        if len(childs2)>0:
            child = random.choice(childs2)
            result = child.simulate()
        elif node.n_sims==0:
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
    # print(root.childs)
    return priority_childs