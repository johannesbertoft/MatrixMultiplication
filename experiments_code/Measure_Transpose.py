from Benchmark import benchmark_transpose, generate_input, write_csv, measure
from MatrixList import transpose


ns, A_lis, B_lis = generate_input(seed=2, n_min=3, n_max=12)

# Benchmark transpose makes a copy before each run so it transposes the same matrix each time. 
means, std = benchmark_transpose(transpose, B_lis, 3)
write_csv(ns, means, std, "measure_transpose/transpose_measure.csv")
