
def reverse_graph(graph):
    rev_graph = [[]] * len(graph)
    for l in graph:
        for edge in l:
            u, v, _, _ = edge
            rev_graph[v] = rev_graph[v] + [((v,u))]

    return rev_graph


def one_index(graph, paths=[]):
    index = {}
    i = 1
    for node in graph:
        for edge in node:
            u, v, a, b = edge
            index[(u,v)] = i
            i +=1

    for path in paths:
        index[tuple(path)] = i
        i+=1

    return index


def weight_fxn(graph, index):
    coeff = [0] * (len(index)+1)
    const = [0] * (len(index)+1)

    for node in graph:
        for edge in node:
            u, v, a, b = edge
            ind = index[(u,v)]
            coeff[ind] = a
            const[ind] = b

    return coeff, const


def remove_flows(graph):
    n = len(graph)
    new_graph = [[]] * n
    for i in range(n):
        new_graph[i] = list(map(lambda (u,v,a,b,f): (u,v,a,b), graph[i]))
    return new_graph


def path_cost(graph, path):
    cost = 0
    for i in range(len(path)-1):
        u,v = path[i], path[i+1]

        for edge in graph[u]:
            u,w,a,b,f = edge
            if w==v:
                cost+=a*(f+1)+b
                break

    return cost

def curr_total_cost(graph, res):
    cost2 = 0
    for node in graph:
        for edge in node:
            u,w,a,b,f = edge
            cost2+=f * (a * f + b)

    return cost2/res

