from __future__ import division
from search import *
from distribution import *
from helpers import curr_total_cost
from paths import find_paths

search_dict = {'u': ucs, 'g': greedy, 'gm': gmaps}

def simulate(theta, users, resolution, search_type):
    graph = [[[0,1, 10/resolution, 0,0], [0,2, 1/resolution, 50,0]], [[1,3, 1/resolution, 50,0], [1,2, 1/resolution, theta,0]], [[2,3, 10/resolution, 0,0]], []]

    search = search_dict[search_type] 
    
    all_results = []
    mean = users * resolution
    p = 0.1
    e = .0000001
    d_list = binomial(mean/p, p, 100000)


    for k in range(users*resolution):
        if search_type=='gm':
            lower_bound = k
            upper_bound = int(mean/p) + 1
            cond_prob_dist = dist_cond(d_list, lower_bound, upper_bound, e)
            search_results = search(graph, cond_prob_dist)

        else: 
            search_results = search(graph)
        all_results.append(search_results)

        path = search_results[1]
        for i in range(len(path)-1):
            for j in range(len(graph[path[i]])):
                if graph[path[i]][j][1] == path[i+1]:
                    graph[path[i]][j][4] += 1
        
    total_cost = curr_total_cost(graph, resolution)
    avg_cost = total_cost/users

    if search_type == 'g':
    	d = min(all_results[-1][0], all_results[-2][0])
    	return d, avg_cost
    else:
    	return search_results[0], avg_cost
