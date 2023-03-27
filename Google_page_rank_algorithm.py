#divide and conquer
import sys
import csv
import time

from product import mult_mat

def get_universe(data):
    """ Get universe size """
    return [row[0].split(";")[0] for row in data]

def get_page_links(page_list):
    """ Get links in page """
    return page_list[0].split(";")[1:]

def transition_matrix(data, alpha, weights=False, prev_page=False):
    """ Compute transition matrix """
    universe=get_universe(data)
    n=len(data)
    if alpha==None: # if none alpha will be computed as a function of the universe size
        alpha = 1 / (n ** 0.5)
    # Transition Matrix initialized with teleporting probabilities:
    # In case of page that links to no page or a group of pages that links to each other    
    M = [[alpha*(1/n) for _ in range(n)] for _ in range(n)]
    for i, page_list in enumerate(data):
        page_links = get_page_links(page_list)
        m = len(page_links)
        # If we want to add weights to pages in top and reduce the importance of last pages
        if weights:
            weights = [(1 - (j / m)) for j in range(-m,m, 2)]
        else:
            weights = [1 for j in range(m)]
        for j, page in enumerate(page_links):
            k = universe.index(page)
            # transition probablity from page i to k
            M[i][k] = M[i][k] + (1 - alpha) * weights[j] / m
            if prev_page: # If we want the inverse link: through the brower you go to previous page
                M[k][i] = M[k][i] + 0.01
    return normalize_matrix(M) 

def normalize_vector(v):
    """ Normalize a vector so the sum of probs. is equal to one """
    s = sum(v)
    return [x / s for x in v]

def normalize_matrix(m):
    """ Normalize a matrix so the sum of probs. in each column is equal to one """
    normalized_rows = []
    for row in m:
        normalized_rows.append(normalize_vector(row))
    return normalized_rows

def distrib_stationnaire(m):
    """ distrib_stationnaire funtion """
    m = list(map(list, zip(*m))) # Transpose
    epsilon=1e-3
    n=len(m)
    vector = [1/n] * n
    v = [0] * n
    v_old = None
    m_old = m
    iter=0
    # e repeat this process as long as the difference between elements in v and vold is greater than ε 
    while v_old is None or max(abs(v[i]-v_old[i]) for i in range(n)) > epsilon:
        iter+=1
        m = mult_mat(m_old, m) # M**(iter+1)
        v_old = v
        v = [sum(m[i][j]*vector[j] for j in range(n)) for i in range(n)] # (M**iter+1)*prob vector
        v = normalize_vector(v) 
    print(f"Number of iterations to converge: {iter} iter")
    return [[u, vi] for vi, u in sorted(zip(v, get_universe(data)) , reverse=True)]
    

if __name__ == "__main__":
    # READ A CSV OF LINKS IN A PAGE IN THE FORMAT OF:
    # PAGE LINK1; LINK2
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    start_time = time.time()
    m=transition_matrix(data, None, True, True)
    result=distrib_stationnaire(m)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Exec Time: {elapsed_time:.6f} seconds")
    with open(f"resultat_{sys.argv[1][:-4]}.txt", "w") as file:
        for sublist in result:
            file.write(sublist[0] + " " + str(sublist[1]) + "\n")

    #RETURNS A PROB OF MOVING FOR EACH PAGE