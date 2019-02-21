##  NOTE: code taken from https://docs.python.org/2/library/heapq.html
##  slightly modified to meet our needs

from heapq import *
from distribution import *

entry_finder = {}               # mapping of nodes to entries
REMOVED = '<removed-node>'      # placeholder for a removed node

def add_node(pq, elt):
    'Add a new node or update the dist of an existing node'
    node = elt[1]
    if node in entry_finder:
        remove_node(node)
    # count = next(counter)
    entry = list(elt)
    entry_finder[node] = entry
    heappush(pq, entry)

def remove_node(node):
    'Mark an existing node as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(node)
    entry[-1] = REMOVED

def pop_node(pq):
    'Remove and return the lowest dist node. Raise KeyError if empty.'
    while pq:
        dist, node = heappop(pq)
        if node is not REMOVED:
            del entry_finder[node]
            return dist, node
    raise KeyError('pop from an empty dist queue')