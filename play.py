import os



from MCTS import *
from utils import *
from game import GameSettings


num_sims = 100
while True:
    GAME = [[0 for _ in range(3)] for _ in range(3)]
    winner = None
    root=None
    history=[[],[]]
    player_i=0
    player_human_i = 1
    os.system("cls")
    inp = input("Enter 1 to play first, q to quit, any other key to play second :")
    try:
        if int(inp)==1:
            player_human_i=0
    except ValueError:
        if len(inp)>0 and inp[0].upper()=='Q':
            break
    while winner is None:
        print_game(GAME,history,player_human_i) 
        if player_i==player_human_i: #human player's turn
            print('Turn : ',GameSettings.players[player_human_i])
            while True:
                valid_options = [i*3+j+1 for i,j in get_childs(GAME)]
                try:
                    inp = int(input("Enter the position where you want to play : "))
                    assert inp in valid_options
                    break
                except Exception:
                    print("Please enter one of ",valid_options)
            inp-=1
            move = (inp//3,inp%3)
            print('\n','*'*60)
        else: #ai's turn
            if root is not None:
                #find the child that matches the current state of the game
                #this was done to make use of information from previous simulations
                try:
                    root = [child for child in root.childs if child.pos==move][0]
                except IndexError:
                    break
            else:
                root = Node(copy.deepcopy(GAME),1-player_human_i)
            root_choices = MCTS_sim(root,num_sims)
            if len(root_choices)==0:
                break
            root = random.choice(root_choices)
            move = root.pos

        GAME[move[0]][move[1]] = GameSettings.players[player_i]
        history[player_i].append(move[0]*3+move[1]+1)
        winner = game_result(GAME)
        if winner is not None:
            break

        player_i=1-player_i

    print_game(GAME,history,0)

    if winner in [-1,None]:
        print("It was a draw.")
    else:
        print("Winner : ",GameSettings.players[winner])

    input("Press Enter")


