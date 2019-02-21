
def find_paths(graph, start=0, end=-1):

	n = len(graph)
	paths = []
	end_list2 = []

	if end == -1:
		end = len(graph)-1
	
	start_vis = [False] * n
	start_vis[0] = True
	nodes = [(start, [start], start_vis)]

	while len(nodes)>0:
		u, path, vis = nodes.pop(0)
		for edge in graph[u]:
			v = edge[1]
			if vis[v] == False and v!= end:
				vis_v = vis[:]
				vis_v[v] = True
				nodes.append((v,path+[v], vis_v))
			elif v==end:
				paths.append(path+[v])

	return paths

def path_to_edge_set(path):
	m = len(path)-1
	s = set(map(lambda i: (path[i], path[i+1]), range(m)))
	# print s
	return s

def paths_through_edge(graph, paths):
	path_edge_sets = {tuple(path): path_to_edge_set(path) for path in paths}

	all_edges = []
	for node in graph:
		all_edges = all_edges+node

	edge_path_sets={key:set() for key in all_edges}
	for edge in all_edges:
		e = (edge[0], edge[1])
		for path in path_edge_sets:
			if e in path_edge_sets[path]:
				edge_path_sets[edge].add(path)

	return edge_path_sets

