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
    print("\tPlayer ",Node.players[player_i]," : ",history[player_i])
    print("\tPlayer ",Node.players[1-player_i]," : ",history[1-player_i])
    print("><"*25,'\n')
    print_board(game)


winner = None
player_i=0
root=None
history=[[],[]]
num_sims = 20
sims_count = 0
while winner is None:
    print_game(GAME)    
    print('Turn : ',Node.players[player_i])
    inp = int(input("Enter the position where you want to play : "))-1
    assert inp<9 and inp>=0
    move = (inp//3,inp%3)
    # print(Node.players[player_i],"'s move:",inp+1)
    print('\n','*'*60)
    GAME[move[0]][move[1]] = Node.players[player_i]
    history[player_i].append(move[0]*3+move[1]+1)
    winner = game_result(GAME)
    if winner is not None:
        break

    print_game(GAME)
    
    # player_i=1-player_i
    if root is not None:
        #find the child that matches the current state of the game
        root = [child for child in root.childs if child.pos==move][0]
        # print_board(root.game)
        #parent = root.parent
        #del parent
        #root.parent = None
    else:
        root = Node(copy.deepcopy(GAME),1-player_i)

    root = MCTS_sim(root,num_sims,sims_count)
    sims_count+=num_sims
    i,j = root.pos

    history[1-player_i].append(i*3+j+1)
    GAME[i][j] = Node.players[1-player_i]
    winner = game_result(GAME)
    if winner is not None:
        break

    input("Press any key for next move")

os.system("cls")
print_game(GAME)
print("Winner : ",winner)


