from collections import defaultdict
class TreeNode:
    def __init__(self,val=None):
        self.val=val
        self.parent=None
        self.children=[]
n=int(input())
val_to_node=defaultdict(TreeNode)
for i in range(n):
    l=list(map(int,input().split()))
    if l[0] not in val_to_node:
        val_to_node[l[0]]=TreeNode(l[0])
    node=val_to_node[l[0]]
    if len(l)==1:
        continue
    for j in range(1,len(l)):
        if l[j] not in val_to_node:
            val_to_node[l[j]]=TreeNode(l[j])
        node.children.append(val_to_node[l[j]])
        val_to_node[l[j]].parent=node
def find_ancestor(node):
    if node.parent is None:
        return node
    return find_ancestor(node.parent)
start=find_ancestor(val_to_node[l[0]])
def small_to_large_sort(node):
    if not node.children:
        return [node.val]
    ans=[]
    l=[]
    l.extend(node.children)
    l.append(node)
    l.sort(key=lambda x: x.val)
    for no in l:
        if no.val==node.val:
            ans.append(no.val)
        else:
            ans.extend(small_to_large_sort(no))
    return ans
print('\n'.join(map(str,small_to_large_sort(start))))


    



