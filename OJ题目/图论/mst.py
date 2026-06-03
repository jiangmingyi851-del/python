import sys
from collections import deque

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n + 1)]
    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))
        adj[u].append(v)
        adj[v].append(u)

    # ---------- 双向链表，维护所有未访问顶点 ----------
    # 哨兵 0 和 n+1，顶点编号 1..n
    nxt = [0] * (n + 2)
    prev = [0] * (n + 2)
    for i in range(1, n + 1):
        nxt[i] = i + 1
        prev[i] = i - 1
    nxt[0] = 1
    prev[1] = 0
    nxt[n] = n + 1
    prev[n + 1] = n
    nxt[n + 1] = n + 1          # 尾哨兵指向自己
    prev[0] = 0

    comp = [0] * (n + 1)        # 每个顶点所属分量编号
    comp_cnt = 0
    q = deque()

    # 当链表非空时，继续寻找新分量
    while nxt[0] != n + 1:
        start = nxt[0]
        # 从链表中删除起点
        p = prev[start]
        nx = nxt[start]
        nxt[p] = nx
        prev[nx] = p
        comp_cnt += 1
        comp[start] = comp_cnt
        q.append(start)

        # BFS 扩展当前分量
        while q:
            u = q.popleft()
            banned = set(adj[u])          # 正权邻居，即补图中不能走的点
            cur = nxt[0]                   # 从第一个未访问顶点开始
            while cur != n + 1:
                nxt_cur = nxt[cur]         # 提前保存下一个，防止删除后丢失
                if cur not in banned:
                    # 删除 cur，加入队列
                    p_cur = prev[cur]
                    q_cur = nxt[cur]
                    nxt[p_cur] = q_cur
                    prev[q_cur] = p_cur
                    comp[cur] = comp_cnt
                    q.append(cur)
                # 若 cur 在 banned 中，则保留，继续检查下一个
                cur = nxt_cur

    # 如果已经全连通，答案为 0
    if comp_cnt == 1:
        print(0)
        return

    # ---------- 收集连接不同分量的正权边 ----------
    cross_edges = []      # (w, comp_u, comp_v)
    for u, v, w in edges:
        cu, cv = comp[u], comp[v]
        if cu != cv:
            cross_edges.append((w, cu, cv))

    # ---------- Kruskal 求分量之间的最小生成树 ----------
    cross_edges.sort()
    parent = list(range(comp_cnt + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    ans = 0
    used = 0
    for w, a, b in cross_edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            ans += w
            used += 1
            if used == comp_cnt - 1:
                break

    print(ans)

if __name__ == "__main__":
    solve()