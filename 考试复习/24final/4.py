from collections import deque
class Node:

    def __init__(self, val):
        self.val = val
        self.left = None

li=list(map(int,input().split()))
li=li[::-1]
stack=deque()
root=None
while li:
    node=Node(li.pop())
    if not root:
        root=node
    else:
        if not stack[0].left:
            stack[0].left=node
        else:
            stack[0].right=node
            stack.popleft()
        stack.append(node)
up=0
down=0
equal=0
def dfs(node,path):
    if not node:
        print(' '.join(path))
        return
    path.append(str(node.val))
    if node.left and node.left.val>node.val:
        global up
        up+=1
    elif node.left and node.left.val<node.val:
        global down
        down+=1
    else:
        global equal
        equal+=1
    if node.right and node.right.val>node.val:
        global up
        up+=1
    elif node.right and node.right.val<node.val:
        global down
        down+=1
    else:
        global equal
        equal+=1
    dfs(node.left,path)
    dfs(node.right,path)
    path.pop()
dfs(root,[])
if up==0:
    print('Max Heap')
elif down==0:
    print('Min Heap')
else:
    print('Not Heap')