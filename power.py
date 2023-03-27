# divide and conquer
import time
import random
import matplotlib.pyplot as plt
def dot_product(m1_row, m2_col):
    return sum([m1_row[i]*m2_col[i] for i in range(len(m1_row))])

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

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

def puissance_mat_naif(m, k):
    if k < 0:
        raise ValueError("The exponent k must be non-negative")
    elif k == 0:
        return identity_matrix(len(m))
    else:
        result = m
        for i in range(k-1):
            result = mult_mat(result, m)
        return result

def puissance_mat_dpr(m, k):
    if k==1:
        return m
    elif k%2==0:
        M=puissance_mat_naif(m, k//2)
        return puissance_mat_naif(M, 2)
    else:
        M=puissance_mat_naif(m, (k-1)//2)
        M=puissance_mat_naif(M, 2)
        return mult_mat(m, M)

def analyze_runtime(Ks):
    m = [[random.randint(0, 9) for j in range(5)] for i in range(5)]

    standard_time = []
    dpr_time = []
    for k in Ks:
        print(f"k: {k}")

        # Standard multiplication
        start_time = time.time()
        result_n = puissance_mat_naif(m, k)
        end_time = time.time()
        elapsed_time = end_time - start_time
        standard_time.append(elapsed_time)
        print(f"Standard power: {elapsed_time:.6f} seconds")
        # Strassen's multiplication
        start_time = time.time()
        result = puissance_mat_dpr(m, k)
        end_time = time.time()
        elapsed_time = end_time - start_time
        dpr_time.append(elapsed_time)
        print(f"dpr_time's power: {elapsed_time:.6f} seconds\n")
    return standard_time, dpr_time

if __name__ == "__main__":
    Ks = [i for i in range(1, 256)]  # powers of 2
    standard_time, strassen_time=analyze_runtime(Ks)
    plt.plot(Ks, standard_time, )
    plt.plot(Ks, strassen_time)
    plt.xlabel('K')
    plt.ylabel('Execution Time (s)')
    plt.legend(['Standard Algorithm', 'DPR Algorithm'])
    plt.savefig("K.jpg")


