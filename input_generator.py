#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:10:44 2021

@author: danielestehghari
"""

from typing import Callable, Any
import time

from MatrixList2 import Matrix, elementary_multiplication, recursive_multiplication_copying, recursive_multiplication_write_through, tiled_multiplication, strassen
import numpy as np
import math
import random

random.seed(42)

def generate_input(n_max):
    
    m = 2**53
    ns = [2**i for i in range(1,n_max+1)]
    A = []
    B = []
    for n in ns:
        x = int(math.sqrt(m/n))
        
        A_floats = [float(i) for i in np.random.randint(-x, x, size=n**2)]
        B_floats = [float(i) for i in np.random.randint(-x, x, size=n**2)]
        
        A.append(Matrix(n,n,A_floats))
        B.append(Matrix(n,n,B_floats))
        
    return A, B
        
if __name__ == '__main__':
    A, B = generate_input(n_max=5)
    print(A[4])
    print(B[4])
