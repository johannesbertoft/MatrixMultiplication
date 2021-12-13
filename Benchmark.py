from typing import Callable, Any, Optional, List, Tuple
import time
import statistics as st
from MatrixList import Matrix, elementary_multiplication, elementary_multiplication_in_place, elementary_multiplication_transposed, recursive_multiplication_copying, recursive_multiplication_write_through, strassen_multithreaded, tiled_multiplication, strassen, transpose
import csv
import random
from input_generator import generate_input
import math

FunType = Callable[[Matrix, Matrix], Matrix]

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

def measure(func: Callable[[], Any]):
    start = time.time()
    func()
    end = time.time()
    return end - start


def benchmark_optimal_param(f: FunType, A: Matrix, B: Matrix, N: int, param: List[int]):
    print("Benchmarking optimal parameter...")
    m: int = len(param)
    M: List[List[int]] = list()
    for i in range(m):
        M.append([])
        for j in range(N): 
            M[i].append(measure(lambda: f(A, B, param[i])))
        log_message(f, A.rows(), M[i][N-1])
    means = [st.mean(n) for n in M]
    stdevs =[st.stdev(n) for n in M]
    return means, stdevs 

def benchmark_runtime(f: FunType, args: Tuple[List[Matrix]], N: int, param = None):
    print("Benchmarking...")
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

def write_csv(ns, means, std, param, filename: str):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Mean", "Standard Deviation", "param"])
        for i in range(len(ns)):
            writer.writerow([ns[i], means[i], std[i], param[i]])

def log_message(f, n, last_run):
    print("Completed measurements for ", f)
    print("Matrices of size: ", n)
    print("Latest runtime: ")
    print(last_run)
    print("----------------------")

def warm_up_cache(funcs, *args):
    print("Warming up the cache...")
    for f in funcs:
        for i in range(len(args[i])-3):
            f(args)

# params = [2**i for i in range(1, 12)]
# print(params)
# ns, A_lis, B_lis = generate_input(seed=2, n_min=1, n_max=10)

# Test best s parameter

all_functions = {
    #elementary_multiplication: "Elementary_Multiplication",
    tiled_multiplication : "Tiled_Multiplication",
    #recursive_multiplication_copying: "Recursive_Copying",
    recursive_multiplication_write_through: "Recursive_Write_Through",
    strassen: "Strassen",
    strassen_multithreaded : "Strassen_Parallel",
    #elementary_multiplication_transposed : "Elementary_Transposed"
    }
# for func in all_functions.keys():
#     results = dict()
#     for i in range(len(A_lis)):
#         lis = list(filter(lambda p: p < A_lis[i].rows(), params))
#         print(lis)
#         means, std = benchmark_optimal_param(func, A_lis[i], B_lis[i], 3, lis)
#         results[A_lis[i].rows()] = means, std
#     write_csv(lis, means, std, "m", f"{all_functions[func]}_n_{A_lis[i].rows()}.csv")



#mean, std = benchmark_runtime(strassen, (A_lis, B_lis), 2, 2)
#benchmark_runtime(elementary_multiplication, (A_lis, B_lis), N=2)
#benchmark_runtime(tiled_multiplication, (A_lis, B_lis), N=2, param=8)
# benchmark_runtime(recursive_multiplication_copying,(A_lis, B_lis), N=2)
#benchmark_runtime(recursive_multiplication_write_through,(A_lis, B_lis), N=2, param=256)
#benchmark_runtime(strassen, (A_lis, B_lis), N=2, param=256)
# benchmark_runtime(strassen_multithreaded, (A_lis, B_lis),N=2, param=256)
# for mat in B_lis:
#     transpose(mat)
# benchmark_runtime(elementary_multiplication_transposed, (A_lis,B_lis), N=2)

#write_csv(ns, mean, std, "test.csv")
