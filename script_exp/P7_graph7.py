import sys
sys.path.append('../')
from algorithm.Alg_Node_Graph import *

def HubsAuthorities(G, epsilon=1e-10):
    n = G.size()
    name2id = G.name2id
    id2name = G.id2name
    pre_a = np.ones(n) / n ** .5
    pre_h = np.ones(n) / n ** .5
    new_a = np.zeros(n)
    new_h = np.zeros(n)
    done  = False
    iter = 0
    while not done:
        for n in G.nodes:
            v = name2id[n]
            new_a[v] = 0
            new_h[v] = 0
            for innode in G.nodes[n].inNode:
                new_a[v] += pre_h[name2id[innode]]
            for outnode in G.nodes[n].outNode:
                new_h[v] += pre_a[name2id[outnode]]
        new_a /= np.dot(new_a, new_a.T) ** .5
        new_h /= np.dot(new_h, new_h.T) ** .5
        err  = np.dot((pre_a - new_a), (pre_a - new_a).T) + \
               np.dot((pre_h - new_h), (pre_h - new_h).T)
        done = err < epsilon
        pre_a = new_a.copy()
        pre_h = new_h.copy()
        iter += 1
    # print('Total iteration:', iter, err)
    out_a = {}
    out_h = {}
    for n, a in zip(id2name, new_a):
        out_a[n] = a
    for n, h in zip(id2name, new_h):
        out_h[n] = h

    return out_a, out_h

def PageRank(G, d=.1, epsilon=1e-10):
    n       = G.size()
    name2id = G.name2id
    id2name = G.id2name
    pre_pr  = np.ones(n) / n ** .5
    new_pr  = np.zeros(n)
    done = False
    iter = 0
    while not done:
        for node in G.nodes:
            v = name2id[node]
            new_pr[v] = 0
            for innode in G.nodes[node].inNode:
                new_pr[v] += pre_pr[name2id[innode]] / len(G.nodes[innode].outNode)
            new_pr[v] = d / n + (1-d) * new_pr[v]
        new_pr /= np.square(new_pr).sum() ** .5
        err  = np.square(pre_pr - new_pr).sum()
        done = err < epsilon
        pre_pr = new_pr.copy()
        iter += 1
    # print('Total iteration:', iter, err)
    out_pr = {}
    for node, pr in zip(id2name, new_pr):
        out_pr[node] = pr
    return out_pr

class SimRank:
    def __init__(self, C):
        self.memo   = None
        self.search = None
        self.c      = C

    def _cal(self, n1, n2):
        origin = self.memo[n1][n2]
        sim = 0
        i   = 0
        for p1 in G.nodes[n1].inNode:
            for p2 in G.nodes[n2].inNode:
                sim += self.memo[p1][p2]
                i   += 1
        if i :       sim *= self.c / i
        self.memo[n1][n2] = self.memo[n2][n1] = sim
        return (origin - sim) * (origin - sim)

    def run(self, G, epsilon=1e-10):
        self.memo   = {}
        self.search = set()
        nodes = list(G.nodes.keys()) #sorted(G.nodes.keys(), key=cmp_to_key(self._cmp))

        # initial
        for n1 in nodes:
            self.memo[n1] = {}
            for n2 in nodes:
                self.memo[n1][n2] = 0.
            self.memo[n1][n1] = 1.

        done = False
        iter = 0
        while not done:
            err = 0
            for i, n1 in enumerate(nodes):
                for n2 in nodes[i+1:]:
                    err += self._cal(n1, n2)
            if err < epsilon: done = True
            iter += 1
            # print('Total iteration:', iter, err)

        return self.memo

def DistanceBaseSimRank(G, C=.2):
    # initial
    A = {}
    for node in G.nodes:
        A[node] = {node: 0.}
        for innode in G.nodes[node].inNode:
            if node == innode: continue
            A[node][innode] = 1.

    # find shortest path
    for midnode in G.nodes:
        for updatenode in list(A[midnode].keys()):
            for node in G.nodes:
                if not midnode in A[node]: continue
                if updatenode in A[node]:
                    if A[node][updatenode] > (A[node][midnode] + A[midnode][updatenode]):
                        A[node][updatenode] = A[node][midnode] + A[midnode][updatenode]
                else:
                    A[node][updatenode] = A[node][midnode] + A[midnode][updatenode]

    # normalize
    for n1 in G.nodes:
        length = 0
        for n2 in A[n1]:
            A[n1][n2] = C ** A[n1][n2]
            length += A[n1][n2] ** 2
        length = length ** .5
        for n2 in A[n1]:
            A[n1][n2] /= length

    # Calculate similarity
    simMatrix = {}
    for n1 in G.nodes:
        simMatrix[n1] = {}
        for n2 in G.nodes:
            sim = 0
            for midnode in A[n1]:
                if midnode in A[n2]:
                    sim += A[n1][midnode] * A[n2][midnode]
            simMatrix[n1][n2] = sim

    return simMatrix

def show(simMatrix):
    def _cmp(a, b):
        if int(a) > int(b): return 1
        else:               return -1

    nodes = sorted(simMatrix.keys(), key=cmp_to_key(_cmp))
    for i, n1 in enumerate(nodes):
        for n2 in nodes[i:]:
            print('SimRank({:s}, {:s}) = {:0.4f}'.format(n1, n2, simMatrix[n1][n2]))
    with open("../output/graph_7/graph_7_SimRank.txt", "w") as output:
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i:]:
                output.write('{:0.4f}'.format(simMatrix[n1][n2]) + ' ')     
            output.write('\n')
         
def Visual(Dict, ntop=5, xlabel='Node', ylabel='Value', title='Authority'):
    def _cmp(a, b):
        if   Dict[a] < Dict[b]: return 1
        elif Dict[b] < Dict[a]: return -1
        else:
            if int(a) > int(b): return 1
            else:               return -1

    i    = 1
    n    = len(Dict)
    ntop = ntop if n > ntop else n
    bars = []
    while n:
        find = False
        while not find:
            try:
                bars.append(Dict[str(i)])
                find = True
            except:
                bars.append(0.)
            i += 1
        n -= 1
    plt.bar(range(1, len(bars) + 1), bars)
    top = sorted(Dict.keys(), key=cmp_to_key(_cmp))
    for i in range(ntop):
        print ('Top{:d} | Node: {:s}| Value: {:0.5f}'.format(i+1, top[i], Dict[top[i]]))
    

    with open("../output/graph_7/graph_7_{:s}.txt".format(title), "w") as output:
        for i in range(ntop):
            output.write( '{:0.5f}'.format(Dict[top[i]]) + ' ')
    a=np.loadtxt("../output/graph_7/graph_7_{:s}.txt".format(title))
    print(title +':')
    print (a)    
    # np.savetxt('001.txt',(Dict[top]),fmt='%.1s')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        default='../hw3dataset/graph_7.txt',
                        dest='FILE',
                        help='Place the input into <file>')

    import numpy as np
    import matplotlib.pyplot as plt
    from functools import cmp_to_key

    args = parser.parse_args()

    G = Graph()
    G.read(args.FILE)
    

    # print(G)
    a, h = HubsAuthorities(G)
    print('Authority:')
    Visual(a, ntop=20, title='HITS_authority')
    
    
    print()
    print('Hub:')
    Visual(h, ntop=20, title='HITS_hub')

    pr = PageRank(G)
    print()
    print('Page Rank:')
    Visual(pr, ntop=20, title='PageRank')

    print()
    print('Similarity Rank:')
    sr = SimRank(C=.8)
    SR = sr.run(G)
    show(SR)

    print()
    print('Distance Base Similarity Rank:')
    DBSR = DistanceBaseSimRank(G)
    show(DBSR)
