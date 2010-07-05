"""
Lifted off:

http://ifdown.net/2007/12/19/simple-applied-ternary-search-tree-in-python
"""

from tst import Node, TST

def path(node, parents, results):
    if parents[node] is None:
        return [node] + results
    else:
        results = [node] + results
        return path(parents[node], parents, results)

def bfs(tst, start, end):
    parents = {}
    seen = {}

    parents[start] = None
    seen[start] = True
    stack = [start]

    while len(stack) > 0:
        node = stack[0]
        stack = stack[1:]
        seen[node] = True
        if node == end:
            return path(node, parents, [])
        else:
            siblings = filter(lambda s: not seen.has_key(s) and s not in stack, tst.near_search(node, 1))
        for n in siblings:
            parents[n] = node
        stack += siblings

    return None

if __name__ == "__main__":
    import time
    tst = TST()
    for word in file('/usr/share/dict/american-english'):
        w = word.strip()
        if w:
            tst.insert(word.strip())
    # simple test
    input = open('test/simple.in')
    start = input.readline().strip()
    end   = input.readline().strip()
    t1 = time.time()
    seq = bfs(tst,start,end)
    print "time: %.2f" % (time.time() - t1)
    for word in seq:
        print word
    # another simple test
    input.close()
    input = open('test/ruby.in')
    start = input.readline().strip()
    end   = input.readline().strip()
    t1 = time.time()
    seq = bfs(tst,start,end)
    print "time: %.2f" % (time.time() - t1)
    for word in seq:
        print word
