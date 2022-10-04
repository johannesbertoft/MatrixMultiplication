import copy
import csv
import math
import random
import statistics as st
import time
from typing import Any, Callable, List, Optional, Tuple, Union

from input_generator import generate_input
from MatrixList import (Matrix, elementary_multiplication,
                        elementary_multiplication_in_place,
                        elementary_multiplication_transposed,
                        recursive_multiplication_copying,
                        recursive_multiplication_write_through, strassen,
                        strassen_multithreaded, tiled_multiplication,
                        transpose)

FunType = Callable[..., Matrix]

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

def measure(func: Callable[[], Any]) -> float:
    start = time.time()
    func()
    end = time.time()
    return end - start


def benchmark_optimal_param(f: FunType, A: Matrix, B: Matrix, N: int, param: List[int]) -> Tuple[List[float], List[float]]:
    print("Benchmarking optimal parameter...")
    m: int = len(param)
    M: List[List[float]] = list()
    for i in range(m):
        M.append([])
        for j in range(N): 
            M[i].append(measure(lambda: f(A, B, param[i])))
        log_message(f, A.rows(), M[i][N-1])
    means = [st.mean(n) for n in M]
    stdevs =[st.stdev(n) for n in M]
    return means, stdevs 

def benchmark_transpose(f: FunType, B_lis: List[Matrix], N: int):
    print("Benchmarking transpose function parameter...")
    m: int = len(B_lis)
    M: List[List[float]] = list()
    for i in range(m):
        M.append([])
        B = B_lis[i]
        for j in range(N):
            B_copy = copy.deepcopy(B) 
            M[i].append(measure(lambda: f(B_copy)))
        log_message(f, B.rows(), M[i][N-1])
    means = [st.mean(n) for n in M]
    stdevs =[st.stdev(n) for n in M]
    return means, stdevs 

def benchmark_runtime(f: FunType, args: Tuple[List[Matrix], List[Matrix]], N: int, param: Union[int, None] = None):
    print("Benchmarking...")
    m: int = len(args[0]) # The number of matrix pairs/triples to compute
    M: List[List[float]] = list()
    A_lis = args[0]
    B_lis = args[1]
    for i in range(m):
        A = A_lis[i] 
        B = B_lis[i]
        M.append([])
        for j in range(N):
            if param is None:
                M[i].append(measure(lambda: f(A, B)))
            else:
                if A.rows() <= param*2:
                    print("parameter: ", A.rows()//2)
                    M[i].append(measure(lambda: f(A, B, A.rows()//2)))
                else:
                    M[i].append(measure(lambda: f(A, B, param)))
        log_message(f, A.rows(), M[i][N-1])
    means = [st.mean(n) for n in M]
    stdevs = [st.stdev(n) for n in M]
    return means, stdevs 

def write_csv_optimal_parameter(ns, means, std, param, filename: str):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Mean", "Standard Deviation", "param"])
        for i in range(len(ns)):
            writer.writerow([ns[i], means[i], std[i], param[i]])

def write_csv(ns, means, std, filename: str):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Mean", "Standard Deviation"])
        for i in range(len(ns)):
            writer.writerow([ns[i], means[i], std[i]])
    f.close()

def log_message(f, n, last_run):
    print("Completed measurements for ", f)
    print("Matrices of size: ", n)
    print("Latest runtime: ")
    print(last_run)
    print("----------------------")

