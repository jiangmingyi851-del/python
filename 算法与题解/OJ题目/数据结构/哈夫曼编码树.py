import heapq
import sys
class Node:
    def __init__(self,val):
        self.val=val
        self.alpha=None
        self.left=None
        self.right=None
def build_huffman_tree(heap):
    while len(heap)>1:
        b1,l1=heapq.heappop(heap)
        b2,l2=heapq.heappop(heap)
        node=Node(b1+b2)
        node.left=l1
        node.right=l2
        node.alpha=l1.alpha.extend(l2.alpha)
        heapq.heappush(heap,(b1+b2,node))
    return heap[0][1]
def huffman_encoding(root,s):
    if not s:
        return ""
    if s in root.left.alpha:
        return "0"+huffman_encoding(root.left,s)
    else:
        return "1"+huffman_encoding(root.right,s)
def huffman_decoding(root,cur_node,s):
    if not s:
        return ""
    if cur_node.left is None and cur_node.right is None:
        return cur_node.alpha[0]+huffman_decoding(root,root,s)
    if s[0]=="0":
        return huffman_decoding(root,cur_node.left,s[1:])
    else:
        return huffman_decoding(root,cur_node.right,s[1:])
        
n=int(input())
heap=[]
for i in range(n):
    a,b=input().split()
    b=int(b)
    no=Node(a)
    no.alpha=[a]
    heapq.heappush(heap,(b,no))
root=build_huffman_tree(heap)
data=sys.stdin.read().split()
it=iter(data)
while True:
    try:
        s=next(it)
        if s[0].isnumeric():
            print(huffman_decoding(root,root,s))
        else:
            print(huffman_encoding(root,s))
    except StopIteration:
        break



    