from MatrixList import *
from Benchmark import *

ns, A_lis, B_lis = generate_input(seed=2, n_min=5, n_max=12)

# Functions without parameter

function_wo_parameter = {
    elementary_multiplication: "Elementary_Multiplication",
    recursive_multiplication_copying: "Recursive_Copying",
}

# Functions with parameter

function_w_parameter = {
    tiled_multiplication : "Tiled_Multiplication",
    strassen: "Strassen",
    strassen_multithreaded : "Strassen_Parallel",
    recursive_multiplication_write_through: "Recursive_Write_Through",
}

# Warming up the cache

print("Warming up the cache....")
for func in function_wo_parameter.keys():
    for i in range(5): # Runs the algorithms until n = 1024
        func(A_lis[i], B_lis[i])
for func in function_w_parameter.keys():
    for i in range(5): # Runs the algorithms until n = 1024
        func(A_lis[i], B_lis[i], 256)
print("Done warming up - race time!")

#Benchmarking without parameter

for f in function_wo_parameter.keys():
    mean, std = benchmark_runtime(f, (A_lis[0:11], B_lis[0:11]), 3)
    write_csv(ns[0:11], mean, std, f'horse_race/{function_wo_parameter[f]}.csv')

# Benchmarking with parameter

for f in function_w_parameter.keys():
    mean, std = benchmark_runtime(f, (A_lis, B_lis), 3, 256) # Benchmarking function controls that if n <= 256 its set to n//2
    write_csv(ns, mean, std, f'horse_race/{function_w_parameter[f]}.csv')

# Transpose operand B before benchmarking transposed

for matrix in B_lis:
    transpose(matrix)

mean, std = benchmark_runtime(elementary_multiplication_transposed, (A_lis, B_lis), 3)
write_csv(ns, mean, std, f'horse_race/Elementary_Transposed.csv')