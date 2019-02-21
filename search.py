from __future__ import division
from heap import *
from helpers import remove_flows, path_cost

def ucs(graph, start=0, end=-1):
    if end == -1:
        end = len(graph)-1

    n = len(graph)
    dist = [0] * n
    for i in range(n):
        if not i == start:
            dist[i] = float('inf')

    h = []
    paths = {}
    paths[0] = [0]

    for i in range(n):
        if i == start:
            add_node(h, (0, start))
        else:
            add_node(h, (float('inf'), i))

    while len(h) > 0:
        try: current = pop_node(h)
        except KeyError: break

        dist[current[1]] = current[0]
        for edge in graph[current[1]]:
            u,v,a,b,f = edge
            w = (a)*(f+1) + b

            if dist[v] > dist[u] + w:
                add_node(h, (dist[u] + w, v))
                paths[v] = paths[u] + [v]
                dist[v] = dist[u] + w
        
        if current[1]==end:
            break

    return (dist[end],paths[end])


def greedy(graph, start=0, end=-1):

    if end == -1:
        end = len(graph)-1

    dead = [False] * len(graph)
    edges = graph[start]
    _, v, a, b, f = min(edges, key=lambda (u,v,a,b,f): (a)*(f+1)+b)
    path = [(start,0), (v, (a)*(f+1)+b)]
    u = v
    while u!= end:
        not_dead = list(filter(lambda x: not dead[x[1]], graph[u]))

        if len(not_dead)==0:
            dead[v] = True
            path.pop()
            u = path[-1]

        else:
            _, v, a,b, f = min(not_dead, key=lambda  (u,v,a,b,f): (a)*(f+1)+b)
            dist = path[-1][1] + (a)*(f+1)+b
            path.append((v,dist))
            u = v

    node_only_path = zip(*path)[0]
    return dist, node_only_path

def gmaps(graph, cond_prob_dist, start=0, end=1):

    no_flow_graph = remove_flows(graph)
    path_costs = exp_costs(no_flow_graph, cond_prob_dist)

    min_exp_cost = float('Inf')
    min_paths = []
    for path in path_costs:
        if path_costs[path] < min_exp_cost:
            min_exp_cost =  path_costs[path]
            min_paths = [path]
        elif path_costs[path] == min_exp_cost:
            min_paths.append(path)

    if len(min_paths)==1:
        return path_cost(graph, min_paths[0]), min_paths[0]
    else:
        min_path = min(min_paths, key=lambda p: path_cost(graph,p))
        return path_cost(graph, min_path), min_path

