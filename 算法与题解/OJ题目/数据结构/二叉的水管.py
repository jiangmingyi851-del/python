# import sys
# from collections import deque
# m,n=map(int,input().split())
# out_degree=[0]*(m+1)
# graph=[[] for i in range(m+1)]
# for i in range(n):
#     l=sys.stdin.readline().strip()
#     u,v=l.split('>')
#     u=int(u.strip())
#     v=int(v.strip())
#     graph[u].append(v)
#     out_degree[v]+=1
# queue=deque()
# canbu=0
# for i in range(1,m+1):
#     if out_degree[i]==0:
#         queue.append(i)
# stack=[]
# while queue:
#     if len(queue)>1:
#         canbu=1
#     u=queue.popleft()
#     stack.append(u)
#     for v in graph[u]:
#         out_degree[v]-=1
#         if out_degree[v]==0:
#             queue.append(v)
# ans=[]    
# def build_tree(preorder):
#     n=len(preorder)
#     if n==0:
#         return []
#     if n==1:
#         return [preorder[0]]
#     root=preorder[0]
#     h=n.bit_length()-1
#     last=n-(2**h-1)
#     left_last=min(last,2**(h-1)) 
#     left_count=(2**(h-1)-1)+left_last 
#     right_count=n-left_count-1
#     right_tree=build_tree(preorder[1:1+right_count])
#     left_tree=build_tree(preorder[1+right_count:])
#     return left_tree+[root]+right_tree

# if len(stack)<m:
#     print('Device error')
#     exit()
# elif canbu==1:
#     print("Not determined.")
#     exit()
# else:
#     ans=build_tree(stack)
#     print(' '.join(map(str,ans)))


# import sys
# from collections import deque

# def solve() -> None:
#     data = sys.stdin.read().strip().split()
#     if not data:
#         return
#     it = iter(data)
#     m = int(next(it))
#     n = int(next(it))
#     # 构建完全二叉树，节点编号 1..m
#     # 树节点索引与输入节点编号是独立的，但这里树节点也用 1..m 表示位置
#     # 计算子树大小
#     size = [0] * (m + 2)  # 多开一点防止越界

#     def calc_size(i: int) -> int:
#         if i > m:
#             return 0
#         left = 2 * i
#         right = 2 * i + 1
#         sz = 1 + calc_size(left) + calc_size(right)
#         size[i] = sz
#         return sz

#     calc_size(1)

#     # 分配排名：左子树所有节点 < 右子树所有节点 < 根
#     rank_val = [0] * (m + 2)  # 排名 1..m，1最小

#     def assign_rank(i: int, start: int) -> None:
#         if i > m:
#             return
#         left = 2 * i if 2 * i <= m else 0
#         right = 2 * i + 1 if 2 * i + 1 <= m else 0
#         L = size[left] if left else 0
#         R = size[right] if right else 0
#         rank_val[i] = start + L + R   # 根节点排名
#         if left:
#             assign_rank(left, start)
#         if right:
#             assign_rank(right, start + L)

#     assign_rank(1, 1)

#     # 中序遍历，得到每个树节点的中序位置（0-indexed）
#     inorder_index = [0] * (m + 2)

#     def inorder_traversal(i: int, idx: list) -> None:
#         if i > m:
#             return
#         left = 2 * i
#         right = 2 * i + 1
#         inorder_traversal(left, idx)
#         inorder_index[i] = idx[0]
#         idx[0] += 1
#         inorder_traversal(right, idx)

#     idx = [0]
#     inorder_traversal(1, idx)

#     # 读入关系
#     graph = [[] for _ in range(m + 1)]
#     indeg = [0] * (m + 1)
#     relations = []  # 保存原始关系用于最后验证

#     for _ in range(n):
#         a = int(next(it))
#         op = next(it)
#         b = int(next(it))
#         if op == '>':
#             # a > b  =>  a -> b
#             graph[a].append(b)
#             indeg[b] += 1
#             relations.append((a, b))
#         # 题目输入只有 '>'，不考虑其他

#     # 拓扑排序（求唯一全序，从大到小）
#     q = deque()
#     for i in range(1, m + 1):
#         if indeg[i] == 0:
#             q.append(i)
#     topo = []
#     unique = True
#     while q:
#         if len(q) > 1:
#             unique = False
#             # 继续处理完以判断环，但一旦不唯一就可以退出？题目要求如果有多种可能就输出Not determined.
#             # 但还需要检查环，所以最好继续处理完，但标记不唯一
#         u = q.popleft()
#         topo.append(u)
#         for v in graph[u]:
#             indeg[v] -= 1
#             if indeg[v] == 0:
#                 q.append(v)
#     # 如果有环，topo长度小于m
#     if len(topo) < m:
#         print("Device error.")
#         return
#     if not unique:
#         print("Not determined.")
#         return

#     # topo 是从大到小的顺序（因为入度为0的是最大）
#     # 反转得到从小到大
#     topo_asc = list(reversed(topo))

#     # 树节点按排名升序（从小到大）
#     sorted_tree = sorted(range(1, m + 1), key=lambda x: rank_val[x])

#     # 映射：节点编号 -> 树节点索引
#     mapping = {}
#     for idx, node_id in enumerate(topo_asc):
#         mapping[node_id] = sorted_tree[idx]



#     # 构建中序遍历结果
#     ans = [0] * m
#     for node_id in range(1, m + 1):
#         tree_node = mapping[node_id]
#         pos = inorder_index[tree_node]
#         ans[pos] = node_id

#     print(' '.join(map(str, ans)))

# if __name__ == "__main__":
#     solve()
import sys
from collections import deque
m,n=map(int,input().split())
out_degree=[0]*(m+1)
graph=[[] for i in range(m+1)]
for i in range(n):
    l=sys.stdin.readline().strip()
    if not l:
        continue
    u,v=l.split('>')
    u=int(u.strip())
    v=int(v.strip())
    graph[u].append(v)
    out_degree[v]+=1
queue=deque()
canbu=0
for i in range(1,m+1):
    if out_degree[i]==0:
        queue.append(i)
stack=[]
while queue:
    if len(queue)>1:
        canbu=1
    u=queue.popleft()
    stack.append(u)
    for v in graph[u]:
        out_degree[v]-=1
        if out_degree[v]==0:
            queue.append(v)
if len(stack)<m:
    print('Device error.')
    exit()
elif canbu==1:
    print("Not determined.")
    exit()
else:
    rank_val=[]
    def root_right_left(u):
        if u>m:
            return
        rank_val.append(u)
        root_right_left(2*u+1)
        root_right_left(2*u)
    root_right_left(1)
    assigned=[0]*(m+1)
    for i in range(m):
        assigned[rank_val[i]]=stack[i]
    ans=[]
    def inorder(u):
        if u>m:
            return
        inorder(2*u)
        ans.append(assigned[u])
        inorder(2*u+1)
    inorder(1)
    print(' '.join(map(str,ans)))

    
    
    