import Matrix
import sys

if __name__ == "__main__":
    first = sys.stdin.readline().split()
    n = int(first[0])
    m = int(first[1])
    order = first[2]
    arr = [int(n) for n in sys.stdin.readline().split()]
    M = Matrix(n, m, order, arr)
    for line in sys.stdin.readlines():
        i, j = [int(x) for x in line.split()]
        print(M.get(i, j))
