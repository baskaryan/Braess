from collections import defaultdict
from numpy.random import poisson, normal, binomial
from paths import find_paths
from equilibrium import *


"""
At any particular person I i am given a lower_bound which 
signifies how many peolpe are already using the graph in total
Lower_bound DOES NOT include that i_th person, so 
dist_cond will start with a number of lower_bound + 1 (such that it includes the i_th person)
"""
def dist_cond(d_list, lower_bound, upper_bound, e):
    #Assuming the first one is the expected number of people, and the other one is the probability
    
    counter = 0
    freq_dict = defaultdict(float)
    for j in range(lower_bound+1, upper_bound+1):
        freq_dict[j] = 0
    for val in d_list:
        if val>lower_bound and val<=upper_bound:
            freq_dict[val] += 1
            counter += 1
    prob_dict = defaultdict(int)
    tot = 0
    for j in range(lower_bound+1, upper_bound+1):  
        prob = float(freq_dict[j])/counter
        if prob > e:     
            prob_dict[j] = prob
            tot += prob

    for j in prob_dict:
        prob_dict[j] = prob_dict[j]/tot

    return prob_dict

'''
Going through all possible total number of people and for each adding the cost
for that particular number multiplied by the conditional probability of obtaining that number
'''  
def exp_costs(graph, cond_prob_dist):
    paths = find_paths(graph)
    paths_cost_dict = defaultdict(float)
    for j in paths:
        paths_cost_dict[tuple(j)] = 0
    
    for F in cond_prob_dist:
        if find_eq_flow(graph, paths, F)==None:
            print F
        flow, eq_paths, non_eq_paths = find_eq_flow(graph, paths, F)
        paths_value_list = find_costs(graph, flow, eq_paths, non_eq_paths)
        for index in range(len(paths_value_list)):
            paths_cost_dict[ tuple(paths_value_list[index][0]) ] += paths_value_list[index][1] * cond_prob_dist[F]
                
    return paths_cost_dict
    

