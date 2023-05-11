import itertools
import copy
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import datetime

def EdmondsKarp(C, E, s, t, n):
    """
        EdmondsKarp Algorithm: Based on this: https://brilliant.org/wiki/edmonds-karp-algorithm/
    """
    flow = 0
    F = [[0 for _ in range(n)] for _ in range(n)]
    while True:
        pathFlow, P = bfs(C, E, s, t, F)
        if pathFlow == 0:
            break
        flow = flow + pathFlow
        v = t
        while v != s:
            u = P[v]
            F[u][v] = F[u][v] + pathFlow
            F[v][u] = F[v][u] - pathFlow
            v = u
    return flow

def bfs(C, E, s, t, F):
    """
        Breadth First Search
    """
    P = [-1 for _ in range(n)]
    M = [0 for _ in range(n)]
    P[s], M[s] = -2, float('inf')
    q = []
    q.append(s)
    while (len(q) > 0):
        u = q.pop(0)
        for v in E[u]:
            if C[u][v] - F[u][v] > 0 and P[v] == -1:
                P[v], M[v]= u, min(M[u], C[u][v] - F[u][v])
                if v == t:
                    return M[t], P
                q.append(v)
    return 0, P

def get_adjacency_list(C):
    """
        Return the adjacency list for a given graph C.
    """
    adj_list = []
    for v in C:
        v_adj_list = []
        for j in range(n):
            if v[j] != 0:
                v_adj_list.append(j)
        adj_list.append(v_adj_list)
    return adj_list

def remove_arcs(C, s, t, arcs_to_remove, n):
    """
        Return the flow given by graph C without k arcs: arcs_to_remove.
    """
    new_C = copy.deepcopy(C)
    for u, v in arcs_to_remove:
        new_C[u][v] = 0
    return EdmondsKarp(new_C, get_adjacency_list(new_C), s, t, n)

def backtrack(C, s, t, min_flow, k, n, results_sorted = False):
    """
        The back track algorithm:
            compute the flow for all possible combinations of arc removals
            return the arcs that give the minmum flow if removed.
            + Possiblity of sorting the arcs  with a score that represents 
              the likelihood that an arc will be part of the solution. 
    """
    arcs = []
    arc_scores = []
    for u in range(n):
        for v in range(n):
            if C[u][v] > 0:
                arcs.append((u,v))
                arc_scores.append(C[u][v] - remove_arcs(C, s, t, [(u,v)], n))
    if results_sorted:
        arcs = [arc for _, arc in sorted(zip(arc_scores, arcs), reverse=True)]
    for arcs_to_remove in itertools.combinations(arcs, k):
        flow = remove_arcs(C, s, t, arcs_to_remove, n)
        if flow < min_flow:
            removed_arcs, min_flow = arcs_to_remove, flow
    return removed_arcs, min_flow

if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        instances = f.readlines()
    n, k = map(int, instances[0].strip().split(";"))
    s = int(instances[1].strip().split(";")[0])
    t = int(instances[-1].strip().split(";")[0])
    C = [[0] * n for _ in range(n)]
    for line in instances[1:]:
        elem = line.strip().split(";")
        u = int(elem[0])
        for v_cap in elem[1:]:
            v, cap = v_cap.strip(")").split("(")
            v, cap = int(v), int(cap)
            C[u][v] = cap
    print("results without sorting:")
    begin_time = datetime.datetime.now()
    arcs = backtrack(C, s, t, float('inf'), k, n)
    print(f"Time for the algorithm to run:{datetime.datetime.now()-begin_time}")
    print("New Max flow:", arcs[1])
    print("Arcs to remove:", arcs[0])
    arcs_out = [f"({str(tpl[0])},{str(tpl[1])})" for tpl in arcs[0]]
    data = pd.DataFrame(arcs_out)
    data.to_csv(f"resultat_{file_name.split('.')[0]}.csv", index=False, header=False)

    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if C[i][j] > 0:
                G.add_edge(i, j, capacity=C[i][j])
    new_C = copy.deepcopy(C)
    for u, v in arcs[0]:
        new_C[u][v] = 0

    G_new = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if new_C[i][j] > 0:
                G_new.add_edge(i, j, capacity=new_C[i][j])
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=200)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G_new, pos, ax=ax, edge_color='r', width=0.8, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): str(d["capacity"]) for (u, v, d) in G.edges(data=True)})
    plt.axis("off")
    plt.savefig(f"resultat_{file_name.split('.')[0]}.png")

    print("results without sorting:")
    arcs = backtrack(C, s, t, float('inf'), k, n, True)
    print("New Max flow:", arcs[1])
    print("Arcs to remove:", arcs[0])

