# divide and conquer
import time
import random
from operator import add
import matplotlib.pyplot as plt
def dot_product(m1_row, m2_col):
    return sum([m1_row[i]*m2_col[i] for i in range(len(m1_row))])

def mult_mat(m1, m2):
    if len(m1[0])==len(m2):
        n_rows, n_cols, n_inner = len(m1), len(m2[0]), len(m1[0])
        m_product = [[0]*n_cols for _ in range(n_rows)]
        for m in range(n_rows):
            for p in range(n_cols):
                m_product[m][p] = dot_product(m1[m], [m2[i][p] for i in range(n_inner)])        
        return m_product
    else:
        raise ValueError(f"Shape mismatch: m1 has {len(m1[0])} columns and m2 has {len(m2)} rows")


def pad_m(m): # To the power of 2
    n_rows, n_cols = len(m), len(m[0])
    padded_rows = 2**(n_rows-1).bit_length() # find the next power of 2 for rows
    padded_cols = 2**(n_cols-1).bit_length() # find the next power of 2 for columns
    if n_rows != padded_rows:
        m += [[0] * n_cols for i in range(padded_rows - n_rows)]
    if n_cols != padded_cols:
        m = [row + [0] * (padded_cols - n_cols) for row in m]
    return m

def unpad_m(m, n_rows, n_cols):
    # Remove the padding from the matrix.
    return [row[:n_cols] for row in m[:n_rows]]

def add_matrices(m1, m2):
    n_rows_m1, n_columns_m1, n_rows_m2, n_columns_m2 = len(m1), len(m1[0]), len(m2), len(m2[0])
    if n_rows_m1 != n_rows_m2 or n_columns_m1 != n_columns_m2:
        raise ValueError("Shape mismatch")
    result = []
    for i in range(n_rows_m1):
        row = []
        for j in range(n_columns_m1):
            row.append(add(m1[i][j], m2[i][j]))
        result.append(row)
    return result

def subtract_matrices(m1, m2):
    n_rows_m1, n_columns_m1, n_rows_m2, n_columns_m2 = len(m1), len(m1[0]), len(m2), len(m2[0])
    if n_rows_m1 != n_rows_m2 or n_columns_m1 != n_columns_m2:
        raise ValueError("Shape mismatch")
    result = []
    for i in range(n_rows_m1):
        row = []
        for j in range(n_columns_m1):
            row.append(m1[i][j] - m2[i][j])
        result.append(row)
    return result

def strassen(m1, m2):
    # Inspired from pseudo code in : http://www.cs.cmu.edu/afs/cs/academic/class/15750-s17/ScribeNotes/lecture1.pdf
    if len(m1) == 1:
        return [[m1[0][0] * m2[0][0]]]
    m1_padded = pad_m(m1)
    m2_padded = pad_m(m2)
    n = len(m1_padded[0])
    m = n // 2
    A = [row[:m] for row in m1_padded[:m]]
    B = [row[m:] for row in m1_padded[:m]]
    C = [row[:m] for row in m1_padded[m:]]
    D = [row[m:] for row in m1_padded[m:]]
    E = [row[:m] for row in m2_padded[:m]]
    F = [row[m:] for row in m2_padded[:m]]
    G = [row[:m] for row in m2_padded[m:]]
    H = [row[m:] for row in m2_padded[m:]]

    S1 = strassen(A, subtract_matrices(F, H))
    S2 = strassen(add_matrices(A, B), H)
    S3 = strassen(add_matrices(C, D), E)
    S4 = strassen(D, subtract_matrices(G, E))
    S5 = strassen(add_matrices(A, D), add_matrices(E, H))
    S6 = strassen(subtract_matrices(B, D), add_matrices(G, H))
    S7 = strassen(subtract_matrices(A, C), add_matrices(E, F))
    m_product_padded = [[0] * n for i in range(len(m1_padded))]
    for i in range(m):
        I0=i+m
        for j in range(m):
            m_product_padded[i][j] = S5[i][j] + S4[i][j] - S2[i][j] + S6[i][j]
            J0=j+m
            m_product_padded[i][J0] = S1[i][J0-m] + S2[i][J0-m]
            m_product_padded[I0][j] = S3[I0-m][j] + S4[I0-m][j]
            J1=j+m
            m_product_padded[I0][J1] = S1[I0-m][J1-m] - S3[I0-m][J1-m] + S5[I0-m][J1-m] - S7[I0-m][J1-m]
    return unpad_m(m_product_padded, len(m1[0]), len(m2[0]))

def strassen_hybride(m1, m2):
    if len(m1)<=64:
        return mult_mat(m1, m2)
    else:
        return strassen(m1, m2)

def analyze_runtime(sizes):
    standard_time = []
    strassen_time = []
    for size in sizes:
        print(f"Size: {size}")
        m1 = [[random.randint(0, 9) for j in range(size)] for i in range(size)]
        m2 = [[random.randint(0, 9) for j in range(size)] for i in range(size)]

        # Standard multiplication
        start_time = time.time()
        result_n = mult_mat(m1, m2)
        end_time = time.time()
        elapsed_time = end_time - start_time
        standard_time.append(elapsed_time)
        print(f"Standard multiplication: {elapsed_time:.6f} seconds")
        # Strassen's multiplication
        start_time = time.time()
        result = strassen(m1, m2)
        end_time = time.time()
        elapsed_time = end_time - start_time
        strassen_time.append(elapsed_time)
        print(f"Strassen's multiplication: {elapsed_time:.6f} seconds\n")
    return standard_time, strassen_time

if __name__ == "__main__":
    sizes = [i for i in range(2, 256)]  # powers of 2
    standard_time, strassen_time=analyze_runtime(sizes)
    plt.plot(sizes, standard_time, )
    plt.plot(sizes, strassen_time)
    plt.xlabel('Input Size')
    plt.ylabel('Execution Time (ms)')
    plt.legend(['Standard Algorithm', 'Strassen Algorithm'])
    plt.savefig("general.jpg")


