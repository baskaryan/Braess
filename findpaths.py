from collections import deque

def find_paths(a_list, start=0, end=-1):

	n = len(a_list)
	paths = []
	end_list2 = []

	if end == -1:
		end = len(a_list)-1
	
	start_vis = [False] * n
	start_vis[0] = True
	nodes = [(start, [start], start_vis)]

	while len(nodes)>0:
		u, path, vis = nodes.pop(0)
		for edge in a_list[u]:
			v = edge[1]
			if vis[v] == False and v!= end:
				vis_v = vis[:]
				vis_v[v] = True
				nodes.append((v,path+[v], vis_v))
			elif v==end:
				paths.append(path+[v])

	return paths