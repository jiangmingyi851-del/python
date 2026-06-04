
s=input()
class Node:
    def __init__(self, val):
        self.val = val
        self.children = []
ptr=[0]
def decode(s):
    if not s:
        return None
    if len(s)==1:
        return Node(s[0])
    node=Node(s[0])
    a=len(s)
    stack=[]
    ptr=2
    i=1
    while i<a:
        if s[i]=='(':
            stack.append('(')
        elif s[i]==')':
            stack.pop()
        if s[i]==',' and len(stack)==1:
            node.children.append(decode(s[ptr:i]))
            ptr=i+1
        if not stack:
            node.children.append(decode(s[ptr:i]))
        i+=1
    return node
def front(node):
    if not node:
        return ''
    if not node.children:
        return node.val   
    ans=[node.val]
    for child in node.children:
        ans.append(front(child))
    return ''.join(ans)
def inorder(node):
    if not node:
        return ''
    if not node.children:
        return node.val
    ans=[]
    for child in node.children:
        ans.append(inorder(child))
    ans.append(node.val)
    return ''.join(ans)
root=decode(s)
print(front(root))
print(inorder(root))

        
