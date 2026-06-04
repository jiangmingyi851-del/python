# from collections import deque
# class Node:
#     def __init__(self, val):
#         self.val = val
#         self.left = None
#         self.right = None
# n = int(input())
# arr = list(map(int, input().split()))
# root = Node(arr[0])
# li=[root]*len(arr)
# for i in range(n.bit_length()-1):
#     for j in range(2**(i+1),2**(i+2)):
#         if j-1>=n:
#             break
#         node=Node(arr[j-1])
#         li[j-1]=node
#         if j%2==0:
#             li[j//2-1].left=node
#         else:
#             li[j//2-1].right=node
# for j in li[::-1]:
#     i=j
#     while i.left or i.right:
#         if i.left and i.left.val>i.val:
#             i.val,i.left.val=i.left.val,i.val
#             i=i.left
#         elif i.right and i.right.val>i.val:
#             i.val,i.right.val=i.right.val,i.val
#             i=i.right
# root=li[0]
# stack=deque([root])
# cur_stack=[]
# while stack:
#     node=stack.popleft()
#     cur_stack.append(node.val)
#     if node.left:
#         stack.append(node.left)
#     if node.right:
#         stack.append(node.right)
# print(' '.join(map(str,cur_stack)))
n=int(input())
arr = list(map(int, input().split()))
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
for i in range(n // 2 - 1, -1, -1):
    heapify(arr, n, i)
print(' '.join(map(str, arr)))




    

