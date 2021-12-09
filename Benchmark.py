from typing import Callable, Any, Optional, List, Tuple
import time
import statistics as st
from MatrixList import Matrix, elementary_multiplication, elementary_multiplication_in_place, elementary_multiplication_transposed, recursive_multiplication_copying, recursive_multiplication_write_through, strassen_multithreaded, tiled_multiplication, strassen, transpose
import csv
import random
from input_generator import generate_input
import math
FunType = Callable[[Matrix, Matrix], Matrix]
N: int = 1


def measure(func: Callable[[], Any]):
    start = time.time()
    func()
    end = time.time()
    return end - start


# def benchmark_optimal_param(f: FunType, A: Matrix, B: Matrix, param: List[int], N: int) -> np.ndarray:
#     m: int = len(param)
#     M: np.ndarray = np.zeros((m, N))
#     for i in range(m):
#         for j in range(N): 
#             M[i, j] = measure(lambda: f(A, B, param[i]))
#     means = np.mean(M, axis=1).reshape(m, 1)
#     stdevs = np.std(M, axis=1, ddof=1).reshape(m, 1)
#     return np.hstack([means, stdevs]) 


def benchmark_runtime(f: FunType, args: Tuple[List[Matrix]], N: int, param = None):
    m: int = len(args[0]) # The number of matrix pairs/triples to compute
    M: List[List[int]] = list()
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
                M[i].append(measure(lambda: f(A, B, param))) 
   
    means = [st.mean(n) for n in M]
    stdevs = [st.stdev(n) for n in M]
    return means, stdevs 


def write_csv(ns, means, std, filename: str):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Mean", "Standard Deviation"])
        for i in range(len(ns)):
            writer.writerow([ns[i], means[i], std[i]])


ns, A_lis, B_lis = generate_input(seed=2, n_min=3, n_max=6)
mean, std = benchmark_runtime(strassen, (A_lis, B_lis), 2, 1)
write_csv(ns, mean, std, "test.csv")
