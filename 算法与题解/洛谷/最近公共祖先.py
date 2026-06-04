from collections import defaultdict
n,m,s=map(int,input().split())
class Node:
    def __init__(self,val):
        self.val=val
        self.father=None
        self.neighbour=[]
nodes=[Node(i) for i in range(n+1)]
root=nodes[s]
for _ in range(n):
    u,v=map(int,input().split())
    nodes[u].neighbour.append(nodes[v])
    nodes[v].neighbour.append(nodes[u])
stack=[root]
while stack:
    node=stack.pop()
    for neighbour in node.neighbour:
        if neighbour.father is None and neighbour!=root:
            neighbour.father=node
            stack.append(neighbour)
layers=defaultdict(int)
layers[root.val]=1
first=[-1]*(n+1)
euler=[]
def dfs(node):
    euler.append(node.val)
    first[node.val]=len(euler)-1
    for neighbour in node.neighbour:
        if neighbour.father==node:
            layers[neighbour.val]=layers[node.val]+1
            dfs(neighbour)
    euler.append(node.val)
dfs(root)
log=
st=[[0]*(2*len(euler)) for _ in range(len(euler))]


        




