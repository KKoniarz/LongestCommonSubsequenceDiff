from numpy import empty


class LCSMatrix:

    def __init__(self, str1, str2):
        self.n = len(str1)
        self.m = len(str2)
        self.str1 = str1
        self.str2 = str2
        self.matrix = empty((self.n + 1, self.m + 1))
        self.subsequences = list()

        for i in range(self.n + 1):
            self.matrix[i][0] = 0
        for j in range(self.m + 1):
            self.matrix[0][j] = 0

        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                if str1[i - 1] == str2[j - 1]:
                    self.matrix[i][j] = self.matrix[i - 1][j - 1] + 1
                else:
                    self.matrix[i][j] = max(self.matrix[i - 1][j], self.matrix[i][j-1])

    def getSubsequencesRecursive(self, x, y, subsequence):
        # base case
        if x == 0 and y == 0:
            if subsequence not in self.subsequences:
                self.subsequences.append(subsequence)
            return
        up_equal = y != 0 and self.matrix[y][x] == self.matrix[y - 1][x]
        left_equal = x != 0 and self.matrix[y][x] == self.matrix[y][x - 1]
        if up_equal:
            self.getSubsequencesRecursive(x, y - 1, subsequence)
        if left_equal:
            self.getSubsequencesRecursive(x - 1, y, subsequence)
        if not up_equal and not left_equal:
            self.getSubsequencesRecursive(x - 1, y - 1, self.str1[y - 1] + subsequence)

    def getSubsequences(self):
        self.subsequences.clear()
        self.getSubsequencesRecursive(self.m, self.n, "")
        return self.subsequences


    def __str__(self):
        return str(self.matrix)
