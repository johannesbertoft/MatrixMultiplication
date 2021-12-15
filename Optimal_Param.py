from Benchmark import benchmark_optimal_param, generate_input, write_csv_optimal_parameter
from MatrixList import tiled_multiplication, recursive_multiplication_write_through, strassen, strassen_multithreaded

functions = {
    tiled_multiplication : "Tiled_Multiplication",
    recursive_multiplication_write_through: "Recursive_Write_Through",
    strassen: "Strassen",
}

params = [2**i for i in range(6, 7)]

ns, A_lis, B_lis = generate_input(seed=2, n_min=11, n_max=11)

for func in functions.keys():
    n = [] 
    mean = []
    stdev = []
    m = []
    for i in range(len(A_lis)):
        lis = list(filter(lambda p: p < A_lis[i].rows(), params)) # Filters params to be the list of params smaller than n
        ns_ = [A_lis[i].rows()]*len(lis)
        means, std = benchmark_optimal_param(func, A_lis[i], B_lis[i], 2, lis)
        n.extend(ns_)
        mean.extend(means)
        stdev.extend(std)
        m.extend(lis)
        print(m)
    write_csv_optimal_parameter(n, mean, stdev, m, f"optimal_parameter/{functions[func]}_optimal_parameter_small.csv")
    
