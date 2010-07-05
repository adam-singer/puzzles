"""
Lifted from:
http://ifdown.net/2007/12/19/simple-applied-ternary-search-tree-in-python
"""

class Node(object):

    def __init__(self, data):
        self.data = data 
        self.left = self.mid = self.right = None

    def __repr__(self):
        return "%s -> (%s, %s, %s)" % (self.data,self.left,self.mid,self.right)

class TST(object):
    """ Ternary Search Tree """

    def __init__(self, root=None):
        self.root = root

    def _rinsert(self, node, remains, orig):
        try:
            if node is None:
                node = Node(remains[0])

            if remains[0] < node.data:
                node.left = self._rinsert(node.left, remains, orig)
            elif remains[0] > node.data:
                node.right = self._rinsert(node.right, remains, orig)
            else:
                node.mid = self._rinsert(node.mid, remains[1:], orig)
        except IndexError:
            node = Node("")
            node.mid = orig
    
        return node

    def insert(self, s):
        assert(len(s) > 0)
        self.root = self._rinsert(self.root, s, s)

    def _rnear_search(self, node, remains, depth, results):
        if node is None or depth < 0:
            return results

        try:
            if depth > 0 or remains[0] < node.data:
                results = self._rnear_search(node.left, remains, depth, results)
      
            if remains[0] == node.data:
                results = self._rnear_search(node.mid,remains[1:],depth,results)
            elif remains[0] != node.data and "" != node.data:
                results = self._rnear_search(
                    node.mid,remains[1:],depth-1,results)

            if depth > 0 or remains[0] > node.data:
                results = self._rnear_search(node.right,remains,depth,results)

        except IndexError:
            if "" == node.data:
                results += [node.mid]

        return results

    def near_search(self, s, d):
        return self._rnear_search(self.root, s, d, [])
