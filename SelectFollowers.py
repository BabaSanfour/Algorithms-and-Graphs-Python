# An algorithm based on Knapsack to select minimum inluencers who will cover all followers
# takes a txt file as input of the form:
"""
X Y
I1 L20 L13 L12

IX ...
"""
# Where X is the number of infleuncers and Y number of total listeners we want to cover
import sys
import datetime
import numpy as np
# Open the instance file and read it in lines format:
# when we access intances using indexing; each index will give us an index. 
with open(sys.argv[1], 'r') as f:
    instances = f.readlines()
idx = instances[0].index(" ") # Get the index of " ", will help us get number of influencers and n listeners 
n_influencers = int(instances[0][0:idx])
n_listerners = int(instances[0][idx:-1])
list_influencers = [] # to save list of influencers names
list_nbre_followers = [] # to save nbre of followers of each influencer
list_followers = [] # to save a list of followers for each influencer
for i in range(1, n_influencers+1):
    inf_line = instances[i]
    idx = inf_line.index(":") # Get the index of ":", will help us get inf name and their followers 
    # inf id
    inf_id =  inf_line[:idx-1]
    list_influencers.append(inf_id)
    # list of followers
    list_foll =  inf_line[idx+2:]
    list_foll = list_foll[:-1].split(" ") # we add -1 to avoid having \n
    list_followers.append(list_foll)
    # number of followers per influencer 
    n_followers = len(list_foll) # number of follwers
    list_nbre_followers.append(n_followers)

# we finished extracting the parameters we need from the instance file now let's build our algorithm
# here we will save the ids of selected influerncers
list_inf_selected = ''
# n_selected will serve as our stppoing condition
n_selected = 0
# if we reach the number of desired listerners we leave the loop

begin_time = datetime.datetime.now()
while (n_selected<n_listerners):
    # get the influencer with the biggest / biggest remaining number of listeners
    nbre_followers_inf = max(list_nbre_followers)
    # add nbre_followers_inf to the number of listerners we got till now
    n_selected+=nbre_followers_inf
    # get the influencer
    max_idx = list_nbre_followers.index(nbre_followers_inf)
    # extract influencer id and add it to our final variable
    list_inf_selected=list_inf_selected+list_influencers[max_idx]+' '
    # get the list of listeners of the influencer
    list_foll_inf = list_followers[max_idx]
    #iterate over all influencers
    for i in range(n_influencers):
        # get their list of follewers
        i_th_list = list_followers[i]
        # get the remaining listerners that the influencer with max listeners don't have
        # in case if i_th influencer == influencer with max listeners we get an empty list
        i_th_list= list(set(i_th_list) - set(list_foll_inf))
        list_followers[i] = i_th_list
        # change the nbre of listeners of each influencer to just remaining listeners
        list_nbre_followers[i] = len(i_th_list)
print(datetime.datetime.now()-begin_time)

with open("resultat_instance_p%s_i%s.txt"%(n_listerners, n_influencers), 'w') as f:
    f.write(list_inf_selected)




