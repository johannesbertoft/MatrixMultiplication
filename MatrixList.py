#!/usr/bin/env python3

#from __future__ import annotations
import math
import multiprocessing
from typing import List, Union, Tuple, overload
import sys
from threading import Thread
from multiprocessing import Process, Pool

class Matrix:
    """
    A list-based implementation of a simple row-major dense matrix with 64-bit
    floating-point elements.
    """
    _rows: int
    _cols: int
    _data: List[float]
    _first_idx: int
    _stride: int

    def __init__(self, rows: int = 0, cols: int = 0,
                 data: List[float] = None,
                 row_length: int = None, first_idx: int = None):
        """
        Constructor for constructing a submatrix given the information of its
        shape and location in the supermatrix.

        Leaving the later arguments out results in a regular
        zero-initialized matrix.
        """
        self._rows = rows
        self._cols = cols
        self._data = [0.0] * (self._cols*self._rows) if data is None else data
        self._stride = cols if row_length is None else row_length
        self._first_idx = 0 if first_idx is None else first_idx

    def rows(self) -> int:
        """
        Returns the number of rows in the matrix
        """
        return self._rows

    def cols(self) -> int:
        """
        Returns the number of columns in the matrix
        """
        return self._cols

    @classmethod
    def from_list(cls, data: List[List[float]]): #-> Matrix:
        """
        Construct a matrix from a list of lists
        """
        rows = len(data)
        cols = len(data[0])
        A = Matrix(rows, cols)
        k = 0
        for i in range(rows):
            for j in range(cols):
                A._data[k] = data[i][j]
                k += 1
        return A

    # these overloads help mypy determine the correct types

    @overload
    def __getitem__(self, key: int) -> float: ...

    @overload
    def __getitem__(self, key: Tuple[slice, slice]): ... # -> Matrix: ...

    @overload
    def __getitem__(self, key: Tuple[int, int]) -> float: ...

    def __getitem__(self, key: Union[int, Tuple[int, int], slice, Tuple[int, slice], Tuple[slice, int], Tuple[slice, slice]]): # -> Union[float, Matrix]:
        """
        Implements the operator A[i,j] supporting also slices for submatrix
        access.

        Note however that the slice support is only partial: the step value is
        ignored.
        """
        if isinstance(key, int):
            return self._data[self._first_idx + (key//self._cols)*self._stride + key % self._cols]
        if isinstance(key, slice):
            stop = key.stop if key.stop is not None else self._rows
            start = key.start if key.start is not None else 0
            return Matrix(stop - start,
                          self._cols,
                          self._data,
                          self._stride,
                          self._first_idx + self._stride*start)
        assert isinstance(key, tuple)
        if isinstance(key[0], int) and isinstance(key[1], int):
            i: int = key[0]
            j: int = key[1]
            return self._data[self._first_idx + i*self._stride + j]
        row_stop: int
        row_start: int
        col_stop: int
        col_start: int
        if isinstance(key[0], slice):
            row_stop = self._rows if key[0].stop is None else key[0].stop
            row_start = 0 if key[0].start is None else key[0].start
        else:
            row_stop = key[0] + 1
            row_start = key[0]
        if isinstance(key[1], slice):
            col_stop = self._cols if key[1].stop is None else key[1].stop
            col_start = 0 if key[1].start is None else key[1].start
        else:
            col_stop = key[1]+1
            col_start = key[1]
        return Matrix(row_stop - row_start,
                      col_stop - col_start,
                      self._data,
                      self._stride,
                      self._first_idx + self._stride*row_start + col_start)

    def __eq__(self, that: object) -> bool:
        """
        Implements the operator ==
        Returns true if and only if the two matrices agree in shape and every
        corresponding element compares equal.
        """
        if not isinstance(that, Matrix):
            return NotImplemented

        if self._rows != that._rows:
            return False
        if self._cols != that._cols:
            return False
        for i in range(self._rows):
            for j in range(self._cols):
                if self[i, j] != that[i, j]:
                    return False
        return True

    def __str__(self) -> str:
        """
        Returns a human-readable representation of the matrix
        """
        return '\n'.join([' '.join([str(self[i, j])
                                    for j in range(self._cols)])
                          for i in range(self._rows)])

    def tolist(self) -> List[List[float]]:
        """
        Returns a list-of-list representation of the matrix
        """
        A: List[List[float]] = list()
        for i in range(self._rows):
            B: List[float] = list()
            for j in range(self._cols):
                c = self[i, j]
                assert isinstance(c, float)
                B.append(c)
            A.append(B)
        return A

    def __setitem__(self, key: Union[int, Tuple[int, int]], value: float) -> None:
        """
        Implements the assignment operator A[i,j] = v supporting also
        one-dimensional flat access.

        Slices are *not* supported.
        """
        if isinstance(key, int):
            self._data[self._first_idx + (key//self._cols)*self._stride +
                       (key % self._cols)] = float(value)
        else:
            assert isinstance(key, tuple)
            i: int
            j: int
            i, j = key
            assert 0 <= i < self._rows
            assert 0 <= j < self._cols
            self._data[self._first_idx + i*self._stride + j] = float(value)


    def __add__(self, that):#: Matrix) -> Matrix:
        """
        Regular addition of two matrices. Does not modify the operands.
        """
        new_data = list()
        for i in range(self.rows()*self.cols()):
            new_data.append(self._data[self._first_idx + (i//self._cols)*self._stride + i % self._cols] + that._data[that._first_idx + (i//that._cols)*that._stride + i % that._cols])
        return Matrix(self.rows(), self.cols(), new_data)

    def __iadd__(self, that):#: Matrix) -> Matrix:
        """
        In-place addition of two matrices, modifies the left-hand side operand.
        """
        for i in range(self.rows()*self.cols()):
            self._data[self._first_idx + (i//self._cols)*self._stride + i % self._cols] += that._data[that._first_idx + (i//that._cols)*that._stride + i % that._cols]
        return self

    def __sub__(self, that):#: Matrix) -> Matrix:
        """
        Regular subtraction of two matrices. Does not modify the operands.
        """
        new_data = list()
        for i in range(self.rows()*self.cols()):
            new_data.append(self._data[self._first_idx + (i//self._cols)*self._stride + i % self._cols] - that._data[that._first_idx + (i//that._cols)*that._stride + i % that._cols])
        return Matrix(self.rows(), self.cols(), new_data)

    def __isub__(self, that):#: Matrix) -> Matrix:
        """
        Regular subtraction of two matrices. Does not modify the operands.
        """
        for i in range(self.rows()*self.cols()):
            self._data[self._first_idx + (i//self._cols)*self._stride + i % self._cols] -= that._data[that._first_idx + (i//that._cols)*that._stride + i % that._cols]
        return self


def split(M: Matrix) ->Tuple[Matrix]:
    rows = M.rows()
    rowsd2 = rows//2
    return M[0:rowsd2, 0:rowsd2], M[0:rowsd2, rowsd2:rows], M[rowsd2:rows, 0:rowsd2], M[rowsd2:rows, rowsd2:rows]


def elementary_multiplication(A: Matrix, B: Matrix) -> Matrix:
    """
    Compute C = AB with three nested loops
    """
    C = Matrix(A.rows(), B.cols(), [0]*(A.rows()*B.cols()))
    for i in range(A.rows()):
        for j in range(A.cols()):
            for k in range(B.cols()):
                C[i, j] += A[i, k] * B[k, j]
    return C


def transpose(A: Matrix) -> None:
    """
    Transposes the matrix in-place
    """
    N = A.rows()
    for n in range(N):
        for m in range(n+1, N):
            A[n, m], A[m, n] = A[m, n], A[n, m]


def elementary_multiplication_transposed(A: Matrix, B: Matrix) -> Matrix:
    """
    Compute C = AB with three nested loops, assuming transposed B
    """
    C = Matrix(A.rows(), B.cols(), [0]*(A.rows()*B.cols()))
    for i in range(A.rows()):
        for j in range(A.cols()):
            for k in range(B.cols()):
                C[i, j] += A[i, k]*B[j, k]
    return C


def tiled_multiplication(A: Matrix, B: Matrix, s: int) -> Matrix:
    """
    Computes C=AB using (n/s)^3 multiplications of size s*s
    """
    C = Matrix(A.rows(), B.cols(), [0]*(A.rows()*B.cols()))
    n: int = C.rows()
    ns: int = n//s
    for i in range(ns):
        for j in range(ns):
            for k in range(ns):
                i_s, j_s, k_s = (i*s, j*s, k*s)
                Cij = C[i_s:i_s+s, j_s:j_s+s]
                Cij += elementary_multiplication(
                    A[i_s:i_s+s, k_s:k_s+s], B[k_s:k_s+s, j_s:j_s+s])
    return C


def elementary_multiplication_in_place(C: Matrix, A: Matrix, B: Matrix) -> None:
    """
    An auxiliary function that computes elementary matrix
    multiplication in place, that is, the operation is C += AB such
    that the product of AB is added to matrix C.
    """
    n = A.rows()
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]


# 

def recursive_multiplication_write_through(A: Matrix, B: Matrix, m: int) -> Matrix:
    """
    Computes C=AB recursively using a write-through strategy. That
    is, no intermediate copies are created; the matrix C is
    initialized as the function is first called, and all updates
    are done in-place in the recursive calls.

    The parameter m controls such that when the subproblem size
    satisfies n <= m, * an iterative cubic algorithm is called instead.
    """
    C = Matrix(A.rows(), B.cols(), [0]*(A.rows()*B.cols()))

    def mult_recursive(A, B, C):
        n = C.rows()
        if n <= m:
            elementary_multiplication_in_place(C, A, B)
        elif n <= 1:
            C[0,0] += A[0,0] * B[0,0]
        else:
            a00, a01, a10, a11 = split(A)
            b00, b01, b10, b11 = split(B)
            c00, c01, c10, c11 = split(C)

            mult_recursive(a00, b00, c00)
            mult_recursive(a01, b10, c00)
            mult_recursive(a00, b01, c01)
            mult_recursive(a01, b11, c01)
            mult_recursive(a10, b00, c10)
            mult_recursive(a11, b10, c10)
            mult_recursive(a10, b01, c11)
            mult_recursive(a11, b11, c11)
        return C
    return mult_recursive(A, B, C)


def recursive_multiplication_copying(A: Matrix, B: Matrix) -> Matrix:
    """
    Computes C=AB by explicitly writing all intermediate
    results. That is, we define the following matrices in terms of
    the operand block matrices:

    P0 = A00
    P1 = A01
    P2 = A00
    P3 = A01
    P4 = A10
    P5 = A11
    P6 = A10
    P7 = A11
    Q0 = B00
    Q1 = B10
    Q2 = B01
    Q3 = B11
    Q4 = B00
    Q5 = B10
    Q6 = B01
    Q7 = B11

    Then compute Mi = Pi*Qi by a recursive application of the function

    Followed by the integration
    C00 = M0 + M1
    C01 = M2 + M3
    C10 = M4 + M5
    C11 = M6 + M7
    """
    n = A.rows()
    if n <= 1:
        return Matrix(n, n, [A[0]*B[0]])
    a00, a01, a10, a11 = split(A)
    b00, b01, b10, b11 = split(B)
    
    M0 = recursive_multiplication_copying(a00, b00)
    M1 = recursive_multiplication_copying(a01, b10)
    M2 = recursive_multiplication_copying(a00, b01)
    M3 = recursive_multiplication_copying(a01, b11)
    M4 = recursive_multiplication_copying(a10, b00)
    M5 = recursive_multiplication_copying(a11, b10)
    M6 = recursive_multiplication_copying(a10, b01)
    M7 = recursive_multiplication_copying(a11, b11)

    C = Matrix(A.rows(), B.cols())
    C00, C01, C10, C11 = split(C)
    C00 += M0 + M1
    C01 += M2 + M3
    C10 += M4 + M5
    C11 += M6 + M7
    return C


def strassen(A: Matrix, B: Matrix, m: int) -> Matrix:
    """
    Computes C=AB using Strassen's algorithm. The structure ought
    to be similar to the copying recursive algorithm. The parameter
    m controls when the routine falls back to a cubic algorithm, as
    the subproblem size satisfies n <= m.
    """
    n = A.rows()
    if n <= m:
        Mi = elementary_multiplication(A, B)
        return Mi

    a11, a12, a21, a22 = split(A) 
    b11, b12, b21, b22 = split(B)
    
    P1 = a11+a22
    Q1 = b11+b22
    P2 = a21+a22
    Q2 = b11
    P3 = a11
    Q3 = b12-b22
    P4 = a22
    Q4 = b21-b11
    P5 = a11+a12
    Q5 = b22
    P6 = a21-a11
    Q6 = b11+b12
    P7 = a12-a22
    Q7 = b21+b22
    
    M1 = strassen(P1, Q1, m)
    M2 = strassen(P2, Q2, m)
    M3 = strassen(P3, Q3, m)
    M4 = strassen(P4, Q4, m)
    M5 = strassen(P5, Q5, m)
    M6 = strassen(P6, Q6, m)
    M7 = strassen(P7, Q7, m)

    C = Matrix(A.rows(), B.cols(), [0]*A.rows()*A.rows())
    C11, C12, C21, C22 = split(C)
    C11 += M1 + M4 - M5 + M7
    C12 += M3 + M5
    C21 += M2 + M4
    C22 += M1 - M2 + M3 + M6
    return C

def strassen_multithreaded(A, B, m: int):
    a11, a12, a21, a22 = split(A) 
    b11, b12, b21, b22 = split(B)
    M: List[Matrix] = [None] * 7
    P = [None] * 7
    Q = [None] * 7
    P[0] = a11+a22
    Q[0] = b11+b22
    P[1] = a21+a22
    Q[1] = b11
    P[2] = a11
    Q[2] = b12-b22
    P[3] = a22
    Q[3] = b21-b11
    P[4] = a11+a12
    Q[4] = b22
    P[5] = a21-a11
    Q[5] = b11+b12
    P[6] = a12-a22
    Q[6] = b21+b22
    args = []
    for i in range(7):
        args.append((P[i], Q[i], m))
    with multiprocessing.Pool(4) as pool:
        M = pool.starmap(strassen, args)
    pool.close()
    pool.join()
    C = Matrix(A.rows(), B.cols())
    C11, C12, C21, C22 = split(C)
    C11 += M[0] + M[3] - M[4] + M[6]
    C12 += M[2] + M[4]
    C21 += M[1] + M[3]
    C22 += M[0] - M[1] + M[2] + M[5]
    #pool.join()
    return C

