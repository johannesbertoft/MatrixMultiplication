#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:10:44 2021

@author: danielestehghari
"""

from MatrixList import Matrix
import math
import random

def generate_input(seed, n_min=1, n_max=1, step=1):
    random.seed(seed)
    m = 2**53
    ns = [2**i for i in range(n_min,n_max+1,step)]
    A = []
    B = []
    
    for n in ns:
        x = int(math.sqrt(m/n))
        
        A_floats = [float(random.randint(-x, x)) for i in range(n**2)]
        B_floats = [float(random.randint(-x, x)) for i in range(n**2)]
        A.append(Matrix(n,n,A_floats))
        B.append(Matrix(n,n,B_floats))
        
    return ns, A, B
