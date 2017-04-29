import threads, sys

# this function parses the command line, making sure all the command line arguments are right
# returns a list
def parseCommandLine():
    if len(sys.argv) is not 6:
        print "Please input commands in the following format:\n"
        print "gol.py file.txt printFlag numThreads rowColFlag printConfigFlag\n"
        print "where printFlag, rowColFlag and printConfigFlag are all 0 or 1"
        sys.stdout.flush() # python equivalent to fflush(stdout) in C
        sys.exit(0)
    elif sys.argv[2] is not in [0,1]:
        print "The second argument must be a 0 or 1\n"
        print "0 will not print the game board after each iteration\n"
        print "1 will print the game board after each iteration"
    elif sys.argv[3]





def main():

main()
