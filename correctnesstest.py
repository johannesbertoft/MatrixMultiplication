#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 12:57:17 2021

@author: danielestehghari
"""

from typing import Callable, Any
import time
import random
from Benchmark import FunType
from MatrixList import Matrix, elementary_multiplication, elementary_multiplication_in_place, elementary_multiplication_transposed, recursive_multiplication_copying, recursive_multiplication_write_through, tiled_multiplication, strassen, strassen_multithreaded, transpose
import math

from input_generator import generate_input

#Matrices = number of large/small matrix-pairs to test, n_small = size of small matrieces, n_large = size of large matrices 
def test_correctness(f: FunType, matrices=20, n_small=2**3, n_large=2**8, param = None): 
    print("Algorithm: {}".format(f.__name__))
    print()
    
    #Small test
    print("Running small test... ")
    x = int(math.sqrt(2**53/n_small))
    for i in range(matrices):
        
        A_floats = [float(random.randint(-x, x)) for i in range(n_small**2)]
        B_floats = [float(random.randint(-x, x)) for i in range(n_small**2)]
       
        A = Matrix(n_small, n_small, A_floats)
        B = Matrix(n_small, n_small, B_floats)
        C = elementary_multiplication(A, B)
        C_shape = A.rows()

        if f == elementary_multiplication_in_place:
            C1 = Matrix(C_shape,C_shape)
            f(C1,A,B)

        elif f == elementary_multiplication_transposed:
            transpose(B)
            C1= f(A,B)
        
        elif param:
            C1 = f(A,B,param)

        else:
            C1 = f(A,B)

        for row in range(C.rows()):
            for col in range(C.cols()):
                if C[row,col] != C1[row,col]:
                    print("Small test failed for matrix size n = {} \n expected value: {}, returned: {}".format(n_small, C[row,col], C1[row,col]))
                    return False
                    
            
    print("Small test (n = {}) with {} matrices sucessful for {}".format(n_small,matrices,f.__name__))
    print()
    print("Running large test...")
    
    #Large test
    x = int(math.sqrt(2**53/n_large))
    for i in range(matrices):
        A_floats = [float(random.randint(-x, x)) for i in range(n_large**2)]
        B_floats = [float(random.randint(-x, x)) for i in range(n_large**2)]
        
        A = Matrix(n_large, n_large, A_floats)
        B = Matrix(n_large, n_large, B_floats)
        C = elementary_multiplication(A, B)
        C_shape = A.rows()
       
        if f == elementary_multiplication_in_place:
            C1 = Matrix(C_shape,C_shape)
            f(C1,A,B)

        elif f == elementary_multiplication_transposed:
            transpose(B)
            C1= f(A,B)
                
        elif param:
            C1 = f(A,B,param)

        else:
            C1 = f(A,B)
        
        for row in range(C.rows()):
            for col in range(C.cols()):
                if C[row,col]!= C1[row,col]:
                    print("Large test failed for matrix size n = {} \n expected value: {}, returned: {}".format(n_large, C[row,col], C1[row,col]))
                    return False
         

    print("Large test (n = {}) with {} matrices succesful for {}".format(n_large,matrices,f.__name__))
    print()
    print()
    return True
    
if __name__ == "__main__":
    args = [20, 2**2, 2**9]
    m = 256
    s = 256

    test_correctness(elementary_multiplication_transposed, *args)
    test_correctness(tiled_multiplication, *args, s)
    test_correctness(elementary_multiplication_in_place, *args)
    test_correctness(recursive_multiplication_write_through, *args, m)
    test_correctness(recursive_multiplication_copying,*args)
    test_correctness(strassen,*args, m)
    test_correctness(strassen_multithreaded,*args, m)

