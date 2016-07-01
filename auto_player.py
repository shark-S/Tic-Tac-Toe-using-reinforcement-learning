import random
import csv
import matplotlib.pyplot as plt

# use 1 for player X/O , 2 for player X/O and 3 for draw and 0 for empty

players = [' ','X','O']

board_print = "----------------------------\n| {0} | {1} | {2} |\n|--------------------------|\n| {3} | {4} | {5} |\n|--------------------------|\n| {6} | {7} | {8} |\n----------------------------"

def emptyboard():
    return [[0,0,0],[0,0,0],[0,0,0]]

def printBoard(board):
    cells = []
    for i in range(3):
        for j in range(3):
            cells.append(players[board[i][j]].center(6))
    print board_print.format(*cells)

def gameover(board):
    for i in range(0,3):
        if board[i][0] !=0 and board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][1]

        if board[0][i] !=0 and board[0][i] == board[1][i] and board[0][i] == board[2][i]:
            return board[0][i]

    if board[0][0] !=0 and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[2][2]

    if board[0][2] !=0 and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[2][0]

    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == 0:
                return 0
    return 3



def find_last(board):
    cntx=0
    cnto=0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == 1:
                cntx += 1
            elif board[i][j] ==2:
                cnto += 1

    if cntx == cnto:
        return 2
    if cntx == (cnto-1):
        return 1
    return -1

def enumstates(board,id,agent):
    if id>8:
        player = find_last(board)
        if player == agent.player:
            agent.add(board)
    else:
        winner = gameover(board)
        if winner != 0:
            return 
        i = id/3
        j = id%3
        for k in range(0,3):
            board[i][j] = k
            enumstates(board,id+1,agent)

class Agent(object):
    def __init__(self,player,lossval=0,learning=True,verbose=False):
        self.player = player
        self.lossval = lossval
        self.alpha  = 0.99
        self.count = 0
        self.pstate = 0
        self.pscore = 0
        self.learning_rate = 0.1 # learning phase
        self.verbose = verbose
        self.values = {}
        self.learning = learning
        enumstates(emptyboard(),0,self)

    def action(self,board):
        r = random.random()
        if r < self.learning_rate:
            move = self.random(board)
            self.log('-------> Explore state: ' +str(move))
        else:
            move = self.greedy_move(board)
            self.log('------> Best move is: '+str(move))

        board[move[0]][move[1]] = self.player
        self.pstate = self.statetuple(board)
        self.pscore = self.check(board)
        board[move[0]][move[1]] = 0
        return move

    def greedy_move(self,board):
        mval = -100000
        mmove = None
        if self.verbose:
            cells = []
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == 0:
                    board[i][j] = self.player
                    val = self.check(board)
                    board[i][j] = 0
                    if val > mval:
                        mval = val
                        mmove = (i,j)
                    if self.verbose:
                        cells.append('{0:3f}'.format(val).center(6))
                elif self.verbose:
                    cells.append(players[board[i][j]].center(6))
        if self.verbose:
            print board_print.format(*cells)
        self.backup(mval)
        return mmove


    def random(self,board):
        current = []
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j]==0:
                    current.append((i,j))
        return random.choice(current)

    def episode_over(self,winner):
        self.backup(self.winnerval(winner))
        self.pstate = None
        self.pscore = 0

    def check(self,board):
        tuples = self.statetuple(board)
        if not tuples in self.values:
            self.add(tuples)
        return self.values[tuples]
        
    #
    def backup(self,nextvalue):
        if self.pstate != None and self.learning:
            self.values[self.pstate] += self.alpha * (nextvalue - self.pscore)

    def add(self,board):
        winner = gameover(board)
        tuples = self.statetuple(board)
        self.values[tuples] = self.winnerval(winner)

    def winnerval(self,winner):
        if winner == self.player:
            return 1
        elif winner == 0:
            return 0.5
        elif winner == 3:
            return 0
        else:
            return self.lossval
    def print_val(self):
        value = deepcopy(self.values)
        for i in value:
            board = [list(i[0]),list(i[1]),list(i[2])]
            cells = []
            for i in range(0,3):
                for j in range(0,3):
                    if board[i][j] == 0:
                        board[i][j] = slef.player
                        cells.append(str(self.check(board)).center(3))
                        board[i][j] = 0
                    else:
                        cells.append(players[board[i][j]].center(3))
            print (board_print.format(*cells))

    def statetuple(self,board):
        return (tuple(board[0]),tuple(board[1]),tuple(board[2]))

    def log(self,st):
        if self.verbose:
            print (st)

class Human(object):
    def __init__(self,player):
        self.player = player

    def action(self,board):
        printBoard(board)
        x = raw_input('Your move?    (i,j) format\n')
        x1 = x.split(',')[0]
        y1 = x.split(',')[1]
        return (int(x1),int(y1))
    def episode_over(self,winner):
        if winner == 3:
            print ('Game Draw')
        else :
            print ('Winner is  player {0}'.format(winner))

def play(agent1,agent2):
    board =emptyboard()
    for i in range(0,9):
        if i%2 ==0:
            move = agent1.action(board)
        else:
            move = agent2.action(board)

        board[move[0]][move[1]] = (i%2)+1

        winner = gameover(board)

        if winner != 0:
            return winner
    return winner

def random_game(agent1,agent2):
    agent1.learning = False
    agent2.learning = False
    e1 = agent1.learning_rate
    e2 = agent2.learning_rate
    agent1.e1 = 0
    agent1.e2 = 0
    r1 = Agent(1)
    r2 = Agent(2)

    r1.learning_rate = 1
    r2.learning_rate = 2
    probs = [0,0,0,0,0,0]
    games = 1000
    for i in range(0,games):
        winner = play(agent1,r2)
        if winner == 1:
            probs[0] += 1.0/games
        elif winner == 2:
            probs[1] += 1.0/games
        else:
            probs[2] += 1.0/games
    for i in range(0,games):
        winner = play(r1,agent2)
        if winner == 2:
            probs[3] += 1.0/games
        elif winner == 1:
            probs[4] += 1.0/games
        else:
            probs[5] += 1.0/games
    agent1.learning_rate = e1
    agent2.learning_rate = e2
    agent1.learning = True
    agent2.learning = True
    return probs

def performance_vs_each_other(agent1,agent2):
    probs = [0,0,0]
    games = 1000
    for i in range(0,games):
        winner = play(agent1,agent2)
        if winner == 1:
            probs[0] +=1.0/games
        elif winner == 2:
            probs[1] += 1.0/games
        else:
            probs[2] += 1.0/games
    return probs

if __name__=="__main__":
    p1 = Agent(1,lossval = -1)
    p2 = Agent(2,lossval = -1)
    r1 = Agent(1,learning=False)

    r2 = Agent(2,learning=False)
    r1.learning_rate = 1
    r2.learning_rate = 1

    conditions = ['P1-win','P1-lose','P1-draw','P2-win','P2-lose','P2-draw']
    colors = ['r','b','g','c','m','b']

    fp = open('data.csv','wb')
    write = csv.writer(fp)
    performance = [[] for _ in range(len(conditions)+1)]
    for i in range(10000
        ):
        if i%1==0:
            print ('Game: {0}'.format(i))
            probs = random_game(p1,p2)
            write.writerow(probs)
            fp.flush()
            performance[0].append(i)
            for id,j in enumerate(probs):
                performance[id+1].append(j)
        winner = play(p1,p2)
        p1.episode_over(winner)
        p2.episode_over(winner)
    fp.close()
    for i in range(1,len(performance)):
        plt.plot(performance[0],performance[i],label=conditions[i-1],color=colors[i-1])
    plt.xlabel('No. of Episodes')
    plt.ylabel('Probability')
    plt.title('RL Agent Performance vs. Random Agent\n({0} loss value, self-play)'.format(p1.lossval))
    plt.legend()
    plt.savefig('Selfplay random_{0}loss.png'.format(p1.lossval))
    
    while 1:
        p2.verbose = True
        p1 = Human(1)
        winner = play(p1,p2)
        p1.episode_over(winner)

p2.episode_over(winner)









