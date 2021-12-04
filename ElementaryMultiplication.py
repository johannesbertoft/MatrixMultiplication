from Matrix import Matrix
import sys

if __name__ == "__main__":
    n, m, p, order = sys.stdin.readline().split()
    n = int(n)
    m = int(m)
    p = int(p)

    arrA = [int(n) for n in sys.stdin.readline().split()]
    arrB = [int(n) for n in sys.stdin.readline().split()]
    A = Matrix(n, m, order, arrA)
    B = Matrix(m, p, order, arrB)
    C = A.multiply(B)
    print(*C.vec)
