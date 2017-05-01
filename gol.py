import thread, sys
import numpy as np

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

def main():
    cmdLineArgs = parseCommandLine()
    file = open(cmdLineArgs[1], "r")
    numRows = int(file.readline())
    numCols = int(file.readline())
    numIterations = int(file.readline())
    numAlive = file.readline()

    game_board = [[0 for x in range(numRows)] for y in range(numCols)]
    for line in file:
        line = line.split()
        game_board[int(line[0])][int(line[1])] = 1
    
    print np.matrix(game_board)
    file.close()
main()
