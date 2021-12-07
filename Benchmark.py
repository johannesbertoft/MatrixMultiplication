from typing import Callable, Any, Optional, List, Tuple
import time
from numpy.lib.index_tricks import s_
from MatrixList import Matrix, elementary_multiplication, elementary_multiplication_in_place, elementary_multiplication_transposed, recursive_multiplication_copying, recursive_multiplication_write_through, tiled_multiplication, strassen, transpose
import numpy as np
import random
import pandas as pd
from input_generator import generate_input

FunType = Callable[[Matrix, Matrix], Matrix]
N: int = 1


def measure(func: Callable[[], Any]):
    start = time.time()
    func()
    end = time.time()
    return end - start


def benchmark_optimal_param(f: FunType, A: Matrix, B: Matrix, param: List[int], N: int) -> np.ndarray:
    m: int = len(param)
    M: np.ndarray = np.zeros((m, N))
    for i in range(m):
        for j in range(N): 
            M[i, j] = measure(lambda: f(A, B, param[i]))
    means = np.mean(M, axis=1).reshape(m, 1)
    stdevs = np.std(M, axis=1, ddof=1).reshape(m, 1)
    return np.hstack([means, stdevs]) 


def benchmark_runtime(f: FunType, args: Tuple[List[Matrix]], N: int, param = None) -> np.ndarray:
    m: int = len(args[0]) # The number of matrix pairs/triples to compute
    M: np.ndarray = np.zeros((m, N))
    A_lis = args[0]
    B_lis = args[1]

    for i in range(m):
        A = A_lis[i] 
        B = B_lis[i]
        print(A)
        for j in range(N):
            if param is None:
                M[i, j] = measure(lambda: f(A, B))
            else:
                M[i, j] = measure(lambda: f(A, B, param))
    means = np.mean(M, axis=1).reshape(m, 1)
    stdevs = np.std(M, axis=1, ddof=1).reshape(m, 1)
    return np.hstack([means, stdevs])




s_list = [2, 4, 8, 16]

Matrices = generate_input(seed=2, n_min=1, n_max=8)

#print(A_lis)


# res = benchmark_optimal_param(tiled_multiplication, A, B, s_list, 3)
# res2 = benchmark_optimal_param(strassen, A, B, s_list, 3)
# res3 = benchmark_optimal_param(recursive_multiplication_write_through, A, B, s_list, 3)

res_run_1 = benchmark_runtime(elementary_multiplication, Matrices, 3)
print(res_run_1)
# df = pd.DataFrame(res, columns=["Mean", "Std"])
# df["s"] = s_list
# print(df)

# Optimal m for recursive copying

# print(A)
# print(B)
# C1 = elementary_multiplication(A, B)
# C2 = recursive_multiplication_write_through(A, B, 2)
# print(C1)
# print("-----------")
# print(C2)
# print("-----------")
# print(C1==C2)
# print("rec copy", measure(lambda: recursive_multiplication_copying(A, B)))
# print("rec write", measure(lambda: recursive_multiplication_write_through(A, B, 2)))
# print("elem", measure(lambda: elementary_multiplication(A, B)))
# print("tiled", measure(lambda: tiled_multiplication(A, B, 2)))
# print("strassen", measure(lambda: strassen(A, B, 2)))
# C = Matrix(n, n)
# print("elem", measure(lambda: elementary_multiplication_in_place(C, A, B)))
# transpose(B)
# print("transposed", measure(lambda: elementary_multiplication_transposed(A, B)))