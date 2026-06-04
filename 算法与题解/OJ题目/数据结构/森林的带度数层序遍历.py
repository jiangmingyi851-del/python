import sys
n=int(input())
ans=[]
def backtrack(node):
    if not node:
        return []
    ans=[]
    if not node.children:
        return [node.val]
    for child in node.children:
        ans.extend(backtrack(child))
    ans.append(node.val)
    return ans
class TreeNode:
    def __init__(self,val):
        self.val=val
        self.children=[]
for r in range(n):
    s=sys.stdin.readline().strip().split()
    stack=[]
    cur_ans=[]
    i=0
    stack.append((b:=TreeNode(s[i]),s[i+1]))
    start=b
    i+=1
    while stack:
        cur_ans.append(stack)
        sa=[]
        for k,j in stack:
            if int(j)>0:
                for l in range(int(j)):
                    i+=1
                    sa.append((c:=TreeNode(s[i]),s[i+1]))
                    k.children.append(c)
                    i+=1
        stack=sa
    ans.extend(backtrack(start))
print(' '.join(ans))
    
    
                

    

        
    