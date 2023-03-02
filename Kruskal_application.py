# Solution to connecting all the possible points in a graph of nodes respecting:
#       - No crossing between the lines 
#       - Basic condition on nodes shape and size
#       - We get the maximum possible distance
# Application on connecting trees in a parc for slackline game. (data can be found here https://quebio.ca/fr/arbresmtl)
# Solution based on the Kruskal algorithm. 

import sys
import pandas as pd
import numpy as np
import datetime

#A function to check of two segments are crossing
#Idea inspired from: https://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
def is_crossing(A, B, C, D):
    # return true if AB and CD are crossing
    A = [data.loc[A,"Coord_X"], data.loc[A,"Coord_Y"]]
    B = [data.loc[B,"Coord_X"], data.loc[B,"Coord_Y"]]
    C = [data.loc[C,"Coord_X"], data.loc[C,"Coord_Y"]]
    D = [data.loc[D,"Coord_X"], data.loc[D,"Coord_Y"]]

    # calculate cross product of (C-A) and (B-A)
    cross1 = (C[0] - A[0]) * (B[1] - A[1]) - (C[1] - A[1]) * (B[0] - A[0])
    # calculate cross product of (D-A) and (B-A)
    cross2 = (D[0] - A[0]) * (B[1] - A[1]) - (D[1] - A[1]) * (B[0] - A[0])
    # calculate cross product of (A-C) and (D-C)
    cross3 = (A[0] - C[0]) * (D[1] - C[1]) - (A[1] - C[1]) * (D[0] - C[0])
    # calculate cross product of (B-C) and (D-C)
    cross4 = (B[0] - C[0]) * (D[1] - C[1]) - (B[1] - C[1]) * (D[0] - C[0])

    # check if both conditions are met
    if cross1 * cross2 < 0 and cross3 * cross4 < 0:
        return True
    else:
        return False

# read csv
data = pd.read_csv(sys.argv[1])
# select only columns we need
data = data[["DHP", "Coord_X", "Coord_Y"]]
# select only trees with width >=25
data = data[data["DHP" ] >=25.0]
# X and Y coordinates are huge which will take a huge shunk of memory and make processing slower
# remove min X from all X column and same for Y
data.Coord_X = data.Coord_X-data.Coord_X.min()
data.Coord_Y = data.Coord_Y-data.Coord_Y.min()
# where we will save the edges
edges = []
# iterate over trees
for counter , i in enumerate(list(data.index)):
    # get tree coordinates
    x1, y1 = data.loc[i,"Coord_X"], data.loc[i,"Coord_Y"]
    #iterate over trees in trees coming after the tree number counter
    for j in ( list(data.index)[counter:]):
        # get coordinates
        x2, y2 = data.loc[j,"Coord_X"], data.loc[j,"Coord_Y"]
        #distance between both trees
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        # if the distance satisfies our conditions we save it + [i, j] 
        if (distance<=30.0) and (distance >= 5.0):
            edges.append([distance, i, j])
# at the end edges is a list relating all possible pairs of trees that satisfies distance conditions and has a width >= 25
# now lets select the pairs that give us the maximum distance for slackline without crossing each other

# here we save selected pairs
selected_pairs=[]
# compute maximum distance
total_dist=0
# Sort edges from Max dist to low dist
edges.sort(reverse=True)
# iterate over all pairs in edges
begin_time = datetime.datetime.now()
for dist, selected_i, selected_j in edges:
    # test will be the funtion that test if we have a crossing
    test=False
    for pair in selected_pairs:
        # iterate over selected pairs
        if  is_crossing(selected_i, selected_j, pair[0], pair[1]): # if there is an intersection between the
            # selected pair and previous selected pairs
            test=True # condition change to True
    # if we dont have an intersection
    if not test:
        # append the pair and add the dist to total dist
        selected_pairs.append([selected_i, selected_j]) 
        total_dist+=dist
# this is just to match trees number to what is asked in homework
for i, pair in enumerate(selected_pairs):
    selected_pairs[i][0], selected_pairs[i][1] = pair[0]+1, pair[1]+1

# create a df using the selected pairs
df = pd.DataFrame(selected_pairs, columns =['A', 'B']) 
# to save output file in required format
columns_titles = ['B', 'A']
df=df.reindex(columns=columns_titles)
df=df.sort_values(by=['B', 'A'])
df.index = np.arange(1, len(df) + 1)
df.to_csv('results_'+sys.argv[1], header=False, sep=' ', index=False)
print(datetime.datetime.now()-begin_time)
print(total_dist)
print(len(selected_pairs))
