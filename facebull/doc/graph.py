#!/usr/bin/python

from dijkstra import shortestPath, prevPath, Dijkstra

shortest = shortestPath
dijk = Dijkstra
prevpath = prevPath

def cross(a,b):
    return set([ (x,y) for x in a for y in b if x != y ])

def getEdges(graph):
    e = set()
    for src in graph.keys():
        e |= cross([src],graph[src].keys())
    return e

def pathCost(p,prices):
    c = 0
    for i in range(len(p) - 1):
        c += prices[(p[i],p[i+1])]
    return c

def reverse(graph):
    rg = {}
    for src in graph:
        for (dst,c) in graph[src].items():
            if dst in rg:
                rg[dst][src] = c
            else:
                rg[dst] = { src : c }
    return rg

def findPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath is not None:
                return newpath
    return None

def copy(g):
    c = {}
    for s in g:
        for d in g[s]:
            if s in c:
                c[s][d] = g[s][d]
            else:
                c[s] = { d : g[s][d] }
    return c

def stronglyConnectedComponents(graph):
    result = []
    stack  = []
    low    = {}
        
    def visit(node):
        if node in low:
            return
    
        num = len(low)
        low[node] = num
        stackPosition = len(stack)
        stack.append(node)
    
        if node in graph:
            for successor in graph[node]:
                visit(successor)
                low[node] = min(low[node], low[successor])
        
        if num == low[node]:
            component = tuple(stack[stackPosition:])
            del stack[stackPosition:]
            result.append(component)
            for item in component:
                low[item] = len(graph)
    
    for node in graph:
        visit(node)
    
    return result

def cost(g):
    return sum( sum(g[v].values()) for v in g )

def facebullCost(g):
    pricetag = 0
    seen = set()
    for s in g:
        dist, prev = dijk(g,s)
        for d in dist:
            p = prevPath(prev,s,d)            
            for i in range(len(p)-1):
                x,y = p[i],p[i+1]
                if (x,y) not in seen:
                    pricetag += g[x][y]
                    seen.add((x,y))
    return pricetag

def load(arcs,weights):
    g = {}
    for (src,dst) in arcs:
        if src in g:
            g[src][dst] = weights[(src,dst)]
        else:
            g[src] = { dst : weights[(src,dst)] }
    return g

def dijkGraph(graph):
    edges = set()
    for src in graph.keys():    
        dist,prev = dijk(graph,src)
        for dst in dist:
            p = prevpath(prev,src,dst)
            for i in range(len(p)-1):
                edges.add((p[i],p[i+1]))
    return edges

"""
def findCycle(NODES, EDGES, READY):
    todo = set(NODES())
    while todo:
        node = todo.pop()
        stack = [node]
        while stack:
            top = stack[-1]
            for node in EDGES(top):
                if node in stack:
                    return stack[stack.index(node):]
                if node in todo:
                    stack.append(node)
                    todo.remove(node)
                    break
            else:
                node = stack.pop()
                READY(node)
    return None
"""

def findAllPaths(graph, start, end, path=[]):
    #http://www.python.org/doc/essays/graphs/
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPaths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def findHamiltonianPaths(graph):
    paths = []
    for startnode in graph:
        for endnode in graph:
            for path in findAllPaths(graph, startnode, endnode):
                if len(path) == len(graph):                    
                    paths.append(path)
    return paths

def findHamiltonianCycles(graph):
    cycles = []
    for startnode in graph:
        for endnode in graph:
            newpaths = findAllPaths(graph, startnode, endnode)
            for path in newpaths:
                if len(path) == len(graph):
                    if path[0] in graph[path[len(graph)-1]]:
                        path.append(path[0])
                        cycles.append(path)
    return cycles

def visualize(G):
    # http://ashitani.jp/gv/
    f = open('dotgraph.txt','w')
    f.writelines('digraph G {\nnode [width=.3,height=.3,shape=octagon,style=filled,color=skyblue];\noverlap="false";\nrankdir="LR";\n')
    f.writelines
    for i in G:
        for j in G[i]:
            s = '      ' + i
            s += ' -- ' +  j 
            s += ';\n'
            f.writelines(s)
            G[j].remove(i)

    f.writelines('}')
    f.close()
    print "done!"

if __name__ == "__main__":

    ##graph = {'1': ['2', '4'],
    ##             '2': ['1', '3','5'],
    ##             '3': ['2','4'],
    ##             '4': ['1','3','5'],
    ##             '5': ['2','4']}
    graph = {'1': ['2', '4','5'],
        '2': ['1', '3','5'],
        '3': ['2','5','6'],
        '4': ['1','7','5'],
        '5': ['1','2','3','4','6','7','8','9'],
        '6': ['3','5','9'],
        '7': ['4','5','8'],
        '8': ['7','5','9'],
        '9': ['8','5','6']}

    print "Finding Hamiltonian Paths----"
    a = findHamiltonianPaths(graph)
    print "Number of Hamiltonian Paths = ", len(a)
    print "Finding Hamiltonian Cycles----"
    a = findHamiltonianCycles(graph)
    print "Number of Hamiltonian Cycles = ", len(a)

    visualize(graph)
