

import sys


class Matrix:

    def __init__(self, n, m, order, arr):
        self.vec = arr
        self.n = n
        self.m = m
        self.order = order

    def get(self, i, j):
        if self.order == 'C':
            return self.vec[i*self.m+j]
        elif self.order == 'F':
            return self.vec[j*self.n+i]

    def set(self, C):
        self.vec = C.vec

    def multiply(self, other):
        if self.order == 'C':
            M = self.__multiplyC(other)
        else:
            M = self.__multiplyF(other)
        return M

    def __multiplyC(self, other):
        C = []
        for i in range(self.n):
            for j in range(other.m):
                c_ij = 0
                for k in range(self.m):
                    c_ij += self.get(i, k) * other.get(k, j)
                C.append(c_ij)
        return Matrix(self.n, other.m, self.order, C)

    def __multiplyF(self, other):
        C = []
        for j in range(other.m):
            for i in range(self.n):
                c_ij = 0
                for k in range(self.m):
                    c_ij += self.get(i, k) * other.get(k, j)
                C.append(c_ij)
        return Matrix(self.n, other.m, self.order, C)

    def partition(self):
        assert(self.order == "C")
        assert(self.n == self.m)
        lis = [[] for i in range(4)]
        for i in range(self.n//2):
            for j in range(self.n//2):
                a00 = self.get(i, j)
                a01 = self.get(i, self.n//2+j)
                a10 = self.get(self.n//2+i, j)
                a11 = self.get(self.n//2+i, self.n//2+j)
                lis[0].append(a00)
                lis[1].append(a01)
                lis[2].append(a10)
                lis[3].append(a11)
        submatrices = [Matrix(self.n//2, self.m//2, "C", lis[i])
                       for i in range(4)]
        self.n = 2
        self.m = 2
        self.vec = submatrices
        # return Matrix(2, 2, "C", submatrices)

    def flatten(self):
        ints = list()
        r = self.vec[0].n
        for i in range(r):
            for m in range(2):
                for j in range(r):
                    ints.append(self.vec[m].get(i, j))
        for i in range(r):
            for m in range(2, 4, 1):
                for j in range(r):
                    ints.append(self.vec[m].get(i, j))
        self.vec = ints

    def add(self, other):
        sumvec = list()
        for i in range(len(self.vec)):
            sumvec.append(self.vec[i] + other.vec[i])
        self.vec = sumvec
        return Matrix(self.n, self.m, "C", sumvec)

    def multiply_recursive(self, other):
        M = list()

        def mult_recursive(A, B, C):
            print(*A.vec)
            print(*B.vec)
            if A.n == 1:
                Mi = A.__multiplyC(B)
                print(*Mi.vec)
                M.append(Mi)
                C.add(Mi)
                return C
            else:
                A.partition()
                B.partition()
                C.partition()
                mult_recursive(A.get(0, 0), B.get(0, 0), C.get(0, 0))
                mult_recursive(A.get(0, 1), B.get(1, 0), C.get(0, 0))
                mult_recursive(A.get(0, 0), B.get(0, 1), C.get(0, 1))
                mult_recursive(A.get(0, 1), B.get(1, 1), C.get(0, 1))
                mult_recursive(A.get(1, 0), B.get(0, 0), C.get(1, 0))
                mult_recursive(A.get(1, 1), B.get(1, 0), C.get(1, 0))
                mult_recursive(A.get(1, 0), B.get(0, 1), C.get(1, 1))
                mult_recursive(A.get(1, 1), B.get(1, 1), C.get(1, 1))
                #print(*[*(C.vec[i].vec[0] for i in range(4))])
                A.flatten()
                B.flatten()
                C.flatten()
                #print(*[*(C.vec[i].vec[0] for i in range(4))])
                print(*C.vec)
                return C
        C = mult_recursive(A, B, Matrix(A.n, A.m, "C", [0]*(n*n)))
        # print(*C.vec)
        return C


n = int(sys.stdin.readline())

A = Matrix(n, n, "C", [int(i) for i in sys.stdin.readline().split()])
B = Matrix(n, n, "C", [int(i) for i in sys.stdin.readline().split()])

C = A.multiply_recursive(B)
