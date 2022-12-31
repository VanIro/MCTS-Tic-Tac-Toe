# MCTS-Tic-Tac-Toe
This repo implements a tic tac toe ai player using Monte Carlo Tree Search algorithm, against which we can play..

## Monte Carlo Tree Search(MCTS)
Unlike minimax algorithm, which needs to create a complete game tree from a game state to take the optimal decision, MCTS just expands the better parts 
of the tree based on a certain number of simulations(the more the better).MCTS is much more computationally efficient than the minimax algorithm(even with $\alpha \beta$ -pruning). The simulation just chooses randomly amongst possible moves and hence no heuristic or any
complex information about the game is required. Also this technique is very general.
                                                                       
In this case, with just 80 simulations per move(it can be reduced further, towards the later stages of the game as there will be less choices to evaluate), the ai is playing very good and I haven't won against it. You are encouraged to try against it...
                                                                        
## Below is a sample of a game:

![image](https://user-images.githubusercontent.com/61639823/210153209-118a39a6-6b4c-4926-86b3-44a6d66fc640.png)

![image](https://user-images.githubusercontent.com/61639823/210153236-c8b70bd8-3f28-4501-a432-3f185a24759b.png)

