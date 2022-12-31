class GameSettings:
    players = [1,2]
    GameChecks = [[(i,j)for j in range(3)] for i in range(3)]+\
        [[(j,i)for j in range(3)] for i in range(3)]+\
        [[(i,i) for i in range(3)]]+[[(i,2-i) for i in range(3)]]