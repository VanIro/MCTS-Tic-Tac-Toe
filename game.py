import os


GAME = [[0 for _ in range(3)] for _ in range(3)]

from MCTS import *


def print_board(game):
    for r,row in enumerate(game):
        for cell in row:
            print(cell, end="\t")
        print("/*\\\t",end='')
        for i in range(3):
            print(i+3*r + 1 if row[i]==0 else 'X', end="\t")
        print('')
    print("="*50)


def print_game(game):
    os.system("cls")
    print("History:")
    print("\tPlayer ",Node.players[player_i],"     : ",history[player_i])
    print("\tPlayer ",Node.players[1-player_i],"<ai> : ",history[1-player_i])
    print("><"*25,'\n')
    print_board(game)


winner = None
player_i=0
root=None
history=[[],[]]
num_sims = 100
while winner is None:
    print_game(GAME)    
    print('Turn : ',Node.players[player_i])
    inp = int(input("Enter the position where you want to play : "))-1
    assert inp<9 and inp>=0
    move = (inp//3,inp%3)
    print('\n','*'*60)
    GAME[move[0]][move[1]] = Node.players[player_i]
    history[player_i].append(move[0]*3+move[1]+1)
    winner = game_result(GAME)
    if winner is not None:
        break

    print_game(GAME)

    if root is not None:
        #find the child that matches the current state of the game
        #this was done to make use of information from previous simulations
        try:
            root = [child for child in root.childs if child.pos==move][0]
        except IndexError:
            break
    else:
        root = Node(copy.deepcopy(GAME),1-player_i)

    root_choices = MCTS_sim(root,num_sims)
    if len(root_choices)==0:
        break
    root = random.choice(root_choices)
    i,j = root.pos

    history[1-player_i].append(i*3+j+1)
    GAME[i][j] = Node.players[1-player_i]
    winner = game_result(GAME)
    if winner is not None:
        break

os.system("cls")
print_game(GAME)

if winner in [-1,None]:
    print("It was a draw.")
else:
    print("Winner : ",Node.players[winner])


