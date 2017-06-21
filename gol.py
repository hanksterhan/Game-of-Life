import thread, sys, os, time
import numpy as np
from struct import *

#Global variables
round_processed = 0
total_processed = 0


# this function parses the command line, making sure all the command line arguments are right
# returns a list containing the file name, printFlag, number of threads, rowColFlag, and printConfigFlag
def parseCommandLine():
    cmdLineArgs = []
    if len(sys.argv) is not 6:
        print "Please input commands in the following format: "
        print "python gol.py file.txt printFlag numThreads rowColFlag printConfigFlag. "
        print "\twhere printFlag, rowColFlag and printConfigFlag are all 0 or 1. "
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    if int(sys.argv[2]) not in [0,1]:
        print "The second argument must be a 0 or 1. "
        print "0 will not print the game board after each iteration, "
        print "1 will print the game board after each iteration. "
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    numThreads = int(sys.argv[3])
    if (not isinstance(numThreads,int)) and sys.argv[3] < 0 :
        print "The third argument must be a number greater than 0. "
        print "This will denote how many threads to create."
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    if int(sys.argv[4]) not in [0,1]:
        print "The fourth argument must be a 0 or 1. "
        print "0 will partition the game board by row. "
        print "1 will partition the game board by column. "
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    if not int(sys.argv[5]) in [0,1]:
        print "The fifth argument must be a 0 or 1. "
        print "0 will not print the partitioning information. "
        print "1 will print the partitioning information. "
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    cmdLineArgs = sys.argv
    return cmdLineArgs

def printTable(game_board, numRows, numCols):
    for r in range(numRows):
        s = ''
        for c in range(numCols):
            if game_board[r][c] is 1:
                s += '@'
            else:
                s += '-'
        print s


#This function takes a 2D array and checks to see which cells should be alive and which cells should be dead
#The function also takes the number of rows, the number of columns, and the row and column of the cell to check.
#returns 0 if the cell is dead, 1 if the cell is alive, and 2 if there is an error
def simulate(game_board, numRows, numCols, row, col):
    neighbors = []
    current_status = game_board[row][col]
    #Upper left case
    if row is 0 and col is 0:
        #Opposite Corner
        neighbors.append(game_board[numRows-1][numCols-1])
        #left
        neighbors.append(game_board[0][numCols-1])
        neighbors.append(game_board[1][numCols-1])
        #top
        neighbors.append(game_board[numRows-1][0])
        neighbors.append(game_board[numRows-1][1])
        #The rest
        neighbors.append(game_board[0][1])
        neighbors.append(game_board[1][1])
        neighbors.append(game_board[1][0])
    #Upper right case
    elif row is 0 and col is (numCols-1):
        #Opposite Corner
        neighbors.append(game_board[numRows-1][0])
        #right
        neighbors.append(game_board[0][0])
        neighbors.append(game_board[1][0])
        #top
        neighbors.append(game_board[numRows-1][numCols-2])
        neighbors.append(game_board[numRows-1][numCols-1])
        #the rest
        neighbors.append(game_board[0][numCols-2])
        neighbors.append(game_board[1][numCols-2])
        neighbors.append(game_board[1][numCols-1])
    #Bottom right case
    elif row is (numRows-1) and col is (numCols-1):
        #Opposite Corner
        neighbors.append(game_board[0][0])
        #right
        neighbors.append(game_board[numRows-2][0])
        neighbors.append(game_board[numRows-1][0])
        #bottom
        neighbors.append(game_board[0][numCols-2])
        neighbors.append(game_board[0][numCols-1])
        #the rest
        neighbors.append(game_board[numRows-2][numCols-2])
        neighbors.append(game_board[numRows-1][numCols-2])
        neighbors.append(game_board[numRows-2][numCols-1])
    #Bottom left case
    elif row is (numRows-1) and col is 0:
        #Opposite Corner
        neighbors.append(game_board[0][numCols-1])
        #left
        neighbors.append(game_board[numRows-2][numCols-1])
        neighbors.append(game_board[numRows-1][numCols-1])
        #bottom
        neighbors.append(game_board[0][0])
        neighbors.append(game_board[0][1])
        #the rest
        neighbors.append(game_board[numRows-2][0])
        neighbors.append(game_board[numRows-2][1])
        neighbors.append(game_board[numRows-1][1])
    #On top wall case
    elif row is 0:
        #top
        neighbors.append(game_board[numRows-1][col-1])
        neighbors.append(game_board[numRows-1][col])
        neighbors.append(game_board[numRows-1][col+1])
        #right
        neighbors.append(game_board[row][col+1])
        #bottom
        neighbors.append(game_board[row+1][col-1])
        neighbors.append(game_board[row+1][col])
        neighbors.append(game_board[row+1][col+1])
        #left
        neighbors.append(game_board[row][col-1])
    #On right wall case
    elif col is (numCols-1):
        #top
        neighbors.append(game_board[row-1][col])
        #right
        neighbors.append(game_board[row-1][0])
        neighbors.append(game_board[row][0])
        neighbors.append(game_board[row+1][0])
        #bottom
        neighbors.append(game_board[row+1][col])
        #left
        neighbors.append(game_board[row-1][col-1])
        neighbors.append(game_board[row][col-1])
        neighbors.append(game_board[row+1][col-1])
    #on bottom wall case
    elif row is (numRows-1):
        #top
        neighbors.append(game_board[row-1][col-1])
        neighbors.append(game_board[row-1][col])
        neighbors.append(game_board[row-1][col+1])
        #right
        neighbors.append(game_board[row][col+1])
        #bottom
        neighbors.append(game_board[0][col-1])
        neighbors.append(game_board[0][col])
        neighbors.append(game_board[0][col+1])
        #left
        neighbors.append(game_board[row][col-1])
    #on left wall case
    elif col is 0:
        #top
        neighbors.append(game_board[row-1][col])
        #right
        neighbors.append(game_board[row-1][col+1])
        neighbors.append(game_board[row][col+1])
        neighbors.append(game_board[row+1][col+1])
        #Bottom
        neighbors.append(game_board[row+1][col])
        #left
        neighbors.append(game_board[row-1][numCols-1])
        neighbors.append(game_board[row][numCols-1])
        neighbors.append(game_board[row+1][numCols-1])
    #Not on a wall case
    else:
        #top
        neighbors.append(game_board[row-1][col-1])
        neighbors.append(game_board[row-1][col])
        neighbors.append(game_board[row-1][col+1])
        #right
        neighbors.append(game_board[row][col+1])
        #bottom
        neighbors.append(game_board[row+1][col-1])
        neighbors.append(game_board[row+1][col])
        neighbors.append(game_board[row+1][col+1])
        #left
        neighbors.append(game_board[row][col-1])
    if current_status is 1:
        #dies from loneliness
        if neighbors.count(1) in [0,1]:
            return 0
        #dies from overpopulation
        elif neighbors.count(1) > 3:
            return 0
    else:
        if neighbors.count(1) is 3:
            return 1
    #If the cell wasn't affected by the neighbors, just return
    return current_status

def main():
    cmdLineArgs = parseCommandLine()

    file = open(cmdLineArgs[1], "r")
    numRows = int(file.readline())
    numCols = int(file.readline())
    numIterations = int(file.readline())
    numAlive = file.readline()


    #Set up the game boards
    game_board = [[0 for x in range(numCols)] for y in range(numRows)]
    game_board_2 = [[0 for x in range(numCols)] for y in range(numRows)]
    for line in file:
        line = line.split()
        game_board[int(line[0])][int(line[1])] = 1

    #start time
    start_time = time.time()
    thread.start_new_thread(threadfunc, args)


    for iterations in range(numIterations):
        for r in range(numRows):
            for c in range(numCols):
                game_board_2[r][c] = simulate(game_board, numRows, numCols, r, c)
        for r in range(numRows):
            for c in range(numCols):
                game_board[r][c] = game_board_2[r][c]
        if int(cmdLineArgs[2]) is 1:
            os.system('cls')
            # print np.matrix(game_board)
            printTable(game_board, numRows, numCols)
            usleep = lambda x: time.sleep(x/1000000.0)
            usleep(100000)
    print "A game board with {0} rows x {1} columns after {2} iterations took {3} seconds to execute".format(numRows,numCols,numIterations,(time.time()-start_time))
    file.close()
main()
