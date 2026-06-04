import sys
data=sys.stdin.read().strip().split()
sys.setrecursionlimit(10**7)
it=iter(data)
class Node:
    def __init__(self,val):
        self.val=val
        self.right=None
        self.left=None
while True:
    try:
        s1,s2=next(it),next(it)
        s2_to_index={c:i for i,c in enumerate(s2)}
        def build(l,r,m,n):
            if l>r:
                return None
            elif l==r:
                return Node(s1[l])
            node=Node(s1[l])
            index=s2_to_index[node.val]
            node.left=build(l+1,l+index-m,m,index-1)
            node.right=build(l+index-m+1,r,index+1,n)
            return node
        root=build(0,len(s1)-1,0,len(s2)-1)
        ans=[]
        def back(node):
            if node.left:
                back(node.left)
            if node.right:
                back(node.right)
            ans.append(node.val)
        back(root)
        print(''.join(ans))
    
    except StopIteration:
        break
import sys

def build(post, pre, ino):
    if not pre:
        return
    root = pre[0]
    idx = ino.index(root)               # 根在中序中的位置
    left_ino = ino[:idx]                # 左子树的中序
    right_ino = ino[idx+1:]             # 右子树的中序
    left_pre = pre[1:1+len(left_ino)]   # 左子树的前序
    right_pre = pre[1+len(left_ino):]   # 右子树的前序
    build(post, left_pre, left_ino)
    build(post, right_pre, right_ino)
    post.append(root)

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    out_lines = []
    for pre, ino in zip(it, it):        # 每两行一组
        post = []
        build(post, pre, ino)
        out_lines.append(''.join(post))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == '__main__':
    main()