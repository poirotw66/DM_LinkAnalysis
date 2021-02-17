class Node:
    def __init__(self):
        self.inNode  = []
        self.outNode = []

    def addIn(self, id):
        self.inNode.append(id)

    def addOut(self, id):
        self.outNode.append(id)

    def __str__(self):
        return 'In  Node: [' + ', '.join(self.inNode) + ']' + '\n' + \
               'Out Node: [' + ', '.join(self.outNode) + ']'

class Graph:
    def __init__(self):
        self.nodes   = {}
        self.name2id = {}
        self.id2name = []

    def _cmp(self, a, b):
        if int(a) > int(b): return 1
        else:               return -1

    def size(self):
        return len(self.nodes)

    def read(self, path):
        with open(path, 'r') as f:
            edges = f.read().split()
            for edge in edges:
                v = edge.split(',')
                # Add Out
                try:
                    self.nodes[v[0]]
                except:
                    self.nodes[v[0]]   = Node()
                    self.name2id[v[0]] = len(self.name2id)
                    self.id2name.append(v[0])
                self.nodes[v[0]].addOut(v[1])
                # Add In
                try:
                    self.nodes[v[1]]
                except:
                    self.nodes[v[1]] = Node()
                    self.name2id[v[1]] = len(self.name2id)
                    self.id2name.append(v[1])
                self.nodes[v[1]].addIn(v[0])

    def __str__(self):
        str = ''
        nodes = sorted(self.nodes.keys(), key=cmp_to_key(self._cmp))
        for n in nodes:
            str += 'Node {:s}'.format(n) + '\n'
            str += self.nodes[n].__str__() + '\n'
        return str[:-1]
