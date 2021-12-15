import glob
import os
import pandas as pd
from pandas.core import algorithms


algorithms = [
    "Elementary_Multiplication",
    "Elementary_Transposed",
    "Recursive_Copying",
    "Recursive_Write_Through",
    "Strassen",
    "Strassen_Parallel",
    "Tiled_Multiplication"
]

transposed = [
    "transpose_measure_Cpython",
    "transpose_measure_pypy"
]

dfs = []
for f in algorithms:
    df = pd.read_csv(f'horse_race/{f}.csv')
    df.to_latex(f'{f}.tex', index=False)
    df["Algorithm"] = f
    dfs.append(df)

result = pd.concat(dfs)
result.index = result["Algorithm"]
result.drop("Algorithm", axis=1)
result.to_csv("results.csv")

for f in transposed:
    df = pd.read_csv(f'measure_transpose/{f}.csv')
    df.to_latex(f'{f}.tex', index=False)