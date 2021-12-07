from typing import Callable, Any
import time
from MatrixList import Matrix, elementary_multiplication, recursive_multiplication_copying, recursive_multiplication_write_through, tiled_multiplication, strassen

def measure(func: Callable[[], Any]):
    start = time.time()
    func()
    end = time.time()
    return end - start
n = 2**8
A = Matrix(n, n, [float(i) for i in range(n**2)])
B = Matrix(n, n, [float(i) for i in range(n**2)])


print("rec copy", measure(lambda: recursive_multiplication_copying(A, B)))
print("rec write", measure(lambda: recursive_multiplication_write_through(A, B, 2)))
print("elem", measure(lambda: elementary_multiplication(A, B)))
print("tiled", measure(lambda: tiled_multiplication(A, B, 2)))
print("strassen", measure(lambda: strassen(A, B, 2)))