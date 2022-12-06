import sys
from LCSMatrix import LCSMatrix

if __name__ == '__main__':
    old_file_name = sys.argv.pop(sys.argv.index("-o") + 1)
    new_file_name = sys.argv.pop(sys.argv.index("-n") + 1)
    print("Comparing " + old_file_name + " to " + new_file_name)
    old_file = open(old_file_name, "r")
    new_file = open(new_file_name, "r")
    mat = LCSMatrix(old_file.read(), new_file.read())
    print(mat)
    print(mat.getSubsequences())
