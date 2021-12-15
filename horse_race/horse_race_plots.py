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

dfs = []
for f in algorithms:
    df = pd.read_csv(f'horse_race/{f}.csv')
    df.to_latex(f'{f}.latex')
    df["Algorithm"] = f
    dfs.append(df)

result = pd.concat(dfs)
result.index = result["Algorithm"]
result.drop("Algorithm", axis=1)
result.to_csv("results.csv")

