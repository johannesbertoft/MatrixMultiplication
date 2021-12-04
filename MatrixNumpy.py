#!/usr/bin/env python3

from __future__ import annotations
from typing import List, Union, Tuple, overload
import numpy as np

class Matrix:
    """
    An implementation of a simple row-major dense matrix with 64-bit
    floating-point elements that uses Numpy as backend.
    """
    _arr: np.ndarray 

    def __init__(self, rows: int = 0, cols: int = 0,
                     data: np.ndarray = None):
        """
        The default constructor. Specifying only rows and columns
        will create a zero-initialized matrix. If data is provided, it
        must conform to the specified rows and columns.
        """
        if data is not None:
            assert data.ndim == 2
            assert data.shape == (rows, cols)
            self._arr = data
        else:
            self._arr = np.zeros((rows,cols), dtype=np.float64)

            

    def rows(self)->int:
        """
        Returns the number of rows in the matrix
        """
        return self._arr.shape[0]


    
    def cols(self)->int:
        """
        Returns the number of columns in the matrix
        """
        return self._arr.shape[1]

    

    @classmethod
    def from_list(cls, data: List[List[float]])->Matrix:
        """
        Construct a matrix from a list of lists
        """
        rows = len(data)
        columns = len(data[0])
        return Matrix(rows,columns,np.array(data))



    # these overloads help mypy determine the correct types
    @overload
    def __getitem__(self, key: int)->float: ...

    @overload
    def __getitem__(self, key: Tuple[slice,slice])->Matrix: ...
        
    @overload
    def __getitem__(self, key: Tuple[int,int])->float: ...


    def __getitem__(self, key: Union[int,Tuple[int,int],slice,Tuple[int,slice], Tuple[slice,int], Tuple[slice,slice]])->Union[float,Matrix]:
        """
        Implements the operator A[i,j] supporting also slices for submatrix 
        access.

        Note however that the slice support is only partial: the step value is 
        ignored.
        """
        if isinstance(key,int):
            return self._arr.ravel()[key]
        if isinstance(key,slice):
            arr = self._arr[key]
            return Matrix(arr.shape[0], arr.shape[1], arr)
        assert isinstance(key,tuple)
        if isinstance(key[0],int) and isinstance(key[1],int):
            return self._arr[key]
        arr = self._arr[key]
        if arr.ndim == 1:
            if isinstance(key[0],int):
                arr = arr.reshape(1,-1)
            elif isinstance(key[1],int):
                arr = arr.reshape(-1,1)
        return Matrix(arr.shape[0], arr.shape[1], arr)

    
    
    def __eq__(self, that: object)->bool:
        """
        Implements the operator ==
        Returns true if and only if the two matrices agree in shape and every
        corresponding element compares equal.
        """
        if not isinstance(that, Matrix):
            return NotImplemented
        return np.array_equal(self._arr, that._arr)
    

    
    def __str__(self)->str:
        """
        Returns a human-readable representation of the matrix
        """
        return str(self._arr)


    def tolist(self)->List[List[float]]:
        """
        Returns a list-of-list representation of the matrix
        """
        return self._arr.tolist()
        


    def __setitem__(self, key: Union[int,Tuple[int,int]], value: float)->None:
        """
        Implements the assignment operator A[i,j] = v supporting also 
        one-dimensional flat access.

        Slices are *not* supported.
        """
        if isinstance(key,int):
            self._arr.ravel()[key] = value
        else:
            self._arr[key] = value

        
            
    def __add__(self, that: Matrix)->Matrix:
        """
        Regular addition of two matrices. Does not modify the operands.
        """
        raise NotImplementedError('Fill in the implementation')



    def __iadd__(self, that: Matrix)->Matrix:
        """
        In-place addition of two matrices, modifies the left-hand side operand.
        """
        raise NotImplementedError('Fill in the implementation')



    def __sub__(self, that: Matrix)->Matrix:
        """
        Regular subtraction of two matrices. Does not modify the operands.
        """
        raise NotImplementedError('Fill in the implementation')



    def __isub__(self, that: Matrix)->Matrix:
        """
        Regular subtraction of two matrices. Does not modify the operands.
        """
        raise NotImplementedError('Fill in the implementation')



def elementary_multiplication(A: Matrix, B: Matrix)->Matrix:
    """
    Compute C = AB with three nested loops
    """
    raise NotImplementedError('Fill in the implementation')



def transpose(A: Matrix)->None:
    """
    Transposes the matrix in-place
    """
    raise NotImplementedError('Fill in the implementation')

            
            
def elementary_multiplication_transposed(A: Matrix, B: Matrix)->Matrix:
    """
    Compute C = AB with three nested loops, assuming transposed B
    """
    raise NotImplementedError('Fill in the implementation')



def tiled_multiplication(A: Matrix, B: Matrix, s: int)->Matrix:
    """
    Computes C=AB using (n/s)^3 multiplications of size s*s
    """
    raise NotImplementedError('Fill in the implementation')



def elementary_multiplication_in_place(C: Matrix, A: Matrix, B: Matrix)->None:
    """
    An auxiliary function that computes elementary matrix
    multiplication in place, that is, the operation is C += AB such
    that the product of AB is added to matrix C.
    """
    raise NotImplementedError('Fill in the implementation')



def recursive_multiplication_copying(A: Matrix, B: Matrix)->Matrix:
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
    raise NotImplementedError('Fill in the implementation')



def recursive_multiplication_write_through(A: Matrix, B: Matrix, m: int)->Matrix:
    """
    Computes C=AB recursively using a write-through strategy. That
    is, no intermediate copies are created; the matrix C is
    initialized as the function is first called, and all updates
    are done in-place in the recursive calls.
     
    The parameter m controls such that when the subproblem size
    satisfies n <= m, * an iterative cubic algorithm is called instead.
    """
    raise NotImplementedError('Fill in the implementation')



def strassen(A: Matrix, B: Matrix, m: int)->Matrix:
    """
    Computes C=AB using Strassen's algorithm. The structure ought
    to be similar to the copying recursive algorithm. The parameter
    m controls when the routine falls back to a cubic algorithm, as
    the subproblem size satisfies n <= m.
    """
    raise NotImplementedError('Fill in the implementation')
