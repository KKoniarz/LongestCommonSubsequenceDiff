from numpy import empty
from termcolor import cprint
from tabulate import tabulate
import os

class LCSMatrix:

    def __init__(self, old, new):
        os.system('color')
        self.o_len = len(old)
        self.n_len = len(new)
        self.old = old
        self.new = new
        self.matrix = empty((self.o_len + 1, self.n_len + 1))
        self.diffOutput = list()

        # Create reference table
        for o_ind in range(0, self.o_len + 1):
            for n_ind in range(0, self.n_len + 1):
                if o_ind == 0 or n_ind == 0:
                    self.matrix[o_ind][n_ind] = 0
                elif old[o_ind - 1] == new[n_ind - 1]:
                    self.matrix[o_ind][n_ind] = self.matrix[o_ind - 1][n_ind - 1] + 1
                else:
                    self.matrix[o_ind][n_ind] = max(self.matrix[o_ind - 1][n_ind], self.matrix[o_ind][n_ind-1])

    def diffRecursive(self, o_ind, n_ind):
        # end of both files
        if o_ind == 0 and n_ind == 0:
            return self.diffOutput.reverse()
        # if reached the end of old file
        # remaining lines were added
        if o_ind == 0:
            # save line as added
            self.diffOutput.append(LCSMatrix.added(self.new[n_ind - 1]))
            # move to the next line of new file
            return self.diffRecursive(o_ind, n_ind - 1)
        # if reached the end of new file
        # remaining lines were removed
        elif n_ind == 0:
            # save line as removed
            self.diffOutput.append(LCSMatrix.removed(self.old[o_ind - 1]))
            # move to the next line of old file
            return self.diffRecursive(o_ind - 1, n_ind)
        # if lines are equal
        elif self.old[o_ind - 1] == self.new[n_ind - 1]:
            # save line as unchanged
            self.diffOutput.append(LCSMatrix.unchanged(self.old[o_ind - 1]))
            # move to the next line for both files
            return self.diffRecursive(o_ind - 1, n_ind - 1)
        # check left and upper cell in the matrix
        # if "=" line was modified we save one line as added and second one as removed
        # moving "=" case to else reverses the order of saving
        # if LCS gets shorter for shorter old file sublist the line was added
        elif self.matrix[o_ind - 1][n_ind] <= self.matrix[o_ind][n_ind - 1]:
            # save line as added
            self.diffOutput.append(LCSMatrix.added(self.new[n_ind - 1]))
            # move to the cell with higher LCS length
            return self.diffRecursive(o_ind, n_ind - 1)
        # if LCS gets shorter for shorter new file sublist the line was removed
        else:
            # save line as removed
            self.diffOutput.append(LCSMatrix.removed(self.old[o_ind - 1]))
            # move to the cell with higher LCS length
            return self.diffRecursive(o_ind - 1, n_ind)

    def diff(self):
        if len(self.diffOutput) == 0:
            self.diffRecursive(self.o_len, self.n_len)

    def getLCSRecursive(self, x, y, subsequence):
        # base case
        if x == 0 or y == 0:
            return subsequence
        up_equal = self.matrix[y][x] == self.matrix[y - 1][x]
        left_equal = self.matrix[y][x] == self.matrix[y][x - 1]
        if up_equal:
            return self.getLCSRecursive(x, y - 1, subsequence)
        elif left_equal:
            return self.getLCSRecursive(x - 1, y, subsequence)
        else:
            return self.getLCSRecursive(x - 1, y - 1, self.old[y - 1] + subsequence)

    def getLCS(self):
        return self.getLCSRecursive(self.n_len, self.o_len, "")

    @staticmethod
    def added(s):
        return "+ " + s

    @staticmethod
    def removed(s):
        return "- " + s

    @staticmethod
    def unchanged(s):
        return "  " + s

    def print(self):
        self.diff()
        for line in self.diffOutput:
            if line[0] == '+':
                cprint(line, "green")
            elif line[0] == '-':
                cprint(line, "red")
            else:
                print(line)

    def printMatrix(self):
        print("Auxiliary table:\n")
        print(tabulate(self.matrix, tablefmt="heavy_grid"))
        print()


    def __str__(self):
        self.diff()
        return str(self.diffOutput)

