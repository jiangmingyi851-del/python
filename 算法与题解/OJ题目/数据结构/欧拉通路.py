# import sys
# from collections import defaultdict
# import heapq
# data=sys.stdin.read().split()
# it=iter(data)
# n=int(next(it))
# for i in range(n):
#     try:
#         t=int(next(it))
#     except StopIteration:
#         break
#     words=[]
#     start_dict=defaultdict(list)
#     end_dict=defaultdict(list)
#     degree_dict=defaultdict(int)
#     for j in range(t):
#         a=next(it)
#         x=a[0]
#         y=a[-1]
#         start_dict[x].append(a)
#         end_dict[y].append(a)
#         degree_dict[x]+=1
#         degree_dict[y]-=1
#         words.append(a)
#     l=0
#     for k in degree_dict:
#         l+=abs(degree_dict[k])
#     if l>2:
#         print('***')
#         break
#     elif l==2:
#         for k in degree_dict:
#             start_dict[k].sort(reverse=True)
#             end_dict[k].sort(reverse=True)
#             if degree_dict[k]==1:
#                 start=start_dict[k][0]
#         ans=[]
#         ans.append(start)
#         def dfs():
#             b=ans[-1][-1]
#             if start_dict[b]:
#                 k=start_dict[b].pop()
#                 ans.append(k)
#                 dfs()
#             return 
#         dfs()
#         if len(ans)<t:
#             print('***')
#             break
#         else:
#             print('->'.join(ans))
#     else:
#         start=start_dict[a].pop()
#         ans=[]
#         def dfs():
#             b=ans[-1][-1]
#             if start_dict[b]:
#                 k=start_dict[b].pop()
#                 ans.append(k)
#                 dfs()
#             return 
#         dfs()
#         if len(ans)<t:
#             print('***')
#             break
#         else:
#             print('->'.join(ans))

import sys

# 增加递归深度以处理 N=1000 的情况
sys.setrecursionlimit(10000)

def solve():
    # 使用 fast I/O 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    it = iter(input_data)
    try:
        t_cases = int(next(it))
    except StopIteration:
        return
    
    for _ in range(t_cases):
        try:
            n = int(next(it))
        except StopIteration:
            break
        
        words = []
        for _ in range(n):
            words.append(next(it))
        
        # 1. 字典序排序
        # 我们希望在 DFS 中先走字典序小的边。
        # 配合 pop()，我们将单词按降序排列，这样 pop() 拿到的就是最小的单词。
        words.sort(reverse=True)
        
        adj = [[] for _ in range(26)]
        in_deg = [0] * 26
        out_deg = [0] * 26
        chars_present = [False] * 26
        
        for w in words:
            u = ord(w[0]) - ord('a')
            v = ord(w[-1]) - ord('a')
            adj[u].append(w)
            out_deg[u] += 1
            in_deg[v] += 1
            chars_present[u] = chars_present[v] = True
            
        # 2. 查找起点并检查度数条件
        start_node = -1
        out_minus_in_1 = 0
        in_minus_out_1 = 0
        possible = True
        
        for i in range(26):
            diff = out_deg[i] - in_deg[i]
            if diff == 1:
                out_minus_in_1 += 1
                start_node = i
            elif diff == -1:
                in_minus_out_1 += 1
            elif diff == 0:
                continue
            else:
                possible = False
                break
        
        # 欧拉通路判别
        if not ((out_minus_in_1 == 0 and in_minus_out_1 == 0) or 
                (out_minus_in_1 == 1 and in_minus_out_1 == 1)):
            possible = False

        if not possible:
            print("***")
            continue

        # 如果是欧拉回路，从最小的具有出度的字符开始
        if start_node == -1:
            for i in range(26):
                if out_deg[i] > 0:
                    start_node = i
                    break
        
        # 3. Hierholzer 算法寻找路径
        res_path = []
        
        def dfs(u):
            curr_adj = adj[u]
            while curr_adj:
                # 弹出当前节点最小的单词（因为之前是 reverse 排序）
                w = curr_adj.pop()
                v = ord(w[-1]) - ord('a')
                dfs(v)
                # 后序加入路径
                res_path.append(w)
        
        if start_node != -1:
            dfs(start_node)
        
        # 4. 连通性检查及输出
        if len(res_path) != n:
            print("***")
        else:
            # 路径是后序添加的，需要反转
            print(".".join(reversed(res_path)))

if __name__ == "__main__":
    solve()


    

    

    

