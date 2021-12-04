from Matrix import Matrix
import sys

if __name__ == "__main__":
    n = int(sys.stdin.readline())
    i, j = [int(x) for x in sys.stdin.readline().split()]
    arr = [int(y) for y in sys.stdin.readline().split()]
    M = Matrix(n, n, "C", arr)
    A = M.partition()
    print(*A.get(i, j))
