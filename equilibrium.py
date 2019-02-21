from helpers import *
from lp import LP 
from copy import deepcopy
from paths import paths_through_edge

def eq_flow(graph, paths, F, start=0, end=-1, removed=[]):
    ## assume edge = (u,v,a,b) where w(f) = af + b 
    if end==-1:
        end = len(graph)-1

    m = sum(map(lambda x: len(x), graph))

    index = one_index(graph, paths)
    coeff, const = weight_fxn(graph, index)

    p = len(paths)
    n = len(graph)
    
    num_constraints = 2 * (p + n + m + 1)
    num_vars = m + p + 1

    pg = LP(num_vars, num_constraints)
    pg.obj[num_vars]=-1

    j=0
    for path in paths:
        
        for k in range(len(path)-1):
            u,v = path[k], path[k+1]
            ind = index[(u,v)]
            
            pg.c[j][ind] = coeff[ind]
            pg.c[j][0] += const[ind]

            pg.c[j+1][ind] = - coeff[ind]
            pg.c[j+1][0] = pg.c[j+1][0] - const[ind]

        pg.c[j][num_vars] = -1
        pg.c[j+1][num_vars] = 1

        j = j+2

    rev_graph = reverse_graph(graph)

    for edge in graph[start]:
        _,v,_,_ = edge
        ind = index[(start,v)]
        pg.c[j][ind] = 1
        pg.c[j+1][ind] = -1

    pg.c[j][0] = -F
    pg.c[j+1][0] = F
    j = j+2

    for edge in rev_graph[end]:
        _,u = edge
        ind = index[(u,end)]
        pg.c[j][ind] =1
        pg.c[j+1][ind] =1

    pg.c[j][0] = -F
    pg.c[j+1][0] = F
    j = j+2

    for k in range(n):
        if k != start and k!= end:
            for out_edge in graph[k]:
                _,v,_,_= out_edge
                ind = index[(k,v)]
                pg.c[j][ind] = 1
                pg.c[j+1][ind] = -1

            for in_edge in rev_graph[k]:
                _,u= in_edge
                ind = index[(u,k)]
                pg.c[j][ind] = -1
                pg.c[j+1][ind] = 1

            j = j+2

    edge_paths_sets = paths_through_edge(graph, paths)
    for node in graph:
        for edge in node:
            u, v, _, _ = edge
            ind = index[(u,v)]
            pg.c[j][ind] = 1
            pg.c[j+1][ind] = -1
            for path in edge_paths_sets[edge]:
                p_ind = index[path]
                pg.c[j][p_ind] = -1
                pg.c[j+1][p_ind] = 1
            j = j+2

    for path in paths:
        ind = index[tuple(path)]
        pg.c[j][ind] = 1
        pg.c[j+1][ind] = -1
    pg.c[j][0] = -F
    pg.c[j+1][0] = F
    j = j+2

    return pg


def find_eq_flow(graph, paths, F, start=0, end=-1):
    if end==-1:
        end = len(graph)-1

    copy_paths = deepcopy(paths)
    flow = eq_flow(graph, copy_paths, F, start, end)
    result = flow.solve()

    if result != "INFEASIBLE" and result != "UNBOUNDED":
        return flow, copy_paths, []

    elif result == "UNBOUNDED":
        return result

    else: 
        best_result=None
        for i in range(len(copy_paths)):
            removed = [copy_paths.pop(0)]

            flow = eq_flow(graph, copy_paths, F, start, end, removed)
            result = flow.solve()

            if result != "INFEASIBLE" and result != "UNBOUNDED":
                if best_result==None:
                    best_result = flow, copy_paths, removed

                elif flow.objval > best_result[0].objval:
                    best_result = flow, copy_paths, removed

            copy_paths = copy_paths + removed

        return best_result


def find_costs(graph, flow, eq_paths, non_eq_paths):
    eq_cost = - round(flow.objval, 6)
    eq_path_costs = list(map(lambda x: (x, eq_cost), eq_paths))

    index = one_index(graph)

    non_eq_costs=[]
    for path in non_eq_paths:
        cost = 0
        for i in range(len(path)-1):
            u,v = path[i], path[i+1]
            ind = index[(u,v)]

            f = round(flow.assignments[ind-1],6)
            coeff, const = weight_fxn(graph, index)

            a,b = coeff[ind], const[ind]
            cost += a * f + b
        non_eq_costs.append(cost)

    result = eq_path_costs + zip(non_eq_paths, non_eq_costs)
    return result


def eq_fxn(graph, paths, F, theta_list, start=0, end=-1):
	if end==-1:
			end = len(graph(0))-1

	c_list = []
	for theta in theta_list:
		g = graph(theta)
		
		flow = find_eq_flow(g, paths, F, start, end)[0]
		c_list.append(-flow.objval)
	return c_list
