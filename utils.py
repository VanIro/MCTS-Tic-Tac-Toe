import os

from game import GameSettings

#returns -1 for draw, index of winner in Node.players if someone has won, else None 
def game_result( game):
    winner=None
    no_draw = False
    for g in GameSettings.GameChecks:
        g_line = [game[gi[0]][gi[1]] for gi in g]
        if all_equal(g_line): winner = g_line[0] if g_line[0] in GameSettings.players else None

        p1, p2 = GameSettings.players
        if not (p1 in g_line and p2 in g_line):
            no_draw = True

        if winner is not None: break
    
    if not no_draw: return -1
    elif winner is not None: return GameSettings.players.index(winner)

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

            print('-' if cell==0 else cell, end="\t")
        print("/*\\\t",end='')
        for i in range(3):
            print(i+3*r + 1 if row[i]==0 else '~', end="\t")
        print('')
    print("="*50)


def print_game(game,history,player_human_i):
    os.system("cls")
    print("History:")
    for i in range(2):
        print("\tPlayer ",GameSettings.players[i], "<you>" if i==player_human_i else "<ai> " ," : ",history[i])
    print("><"*25,'\n')
    print_board(game)