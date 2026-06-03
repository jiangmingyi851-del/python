下面以一棵有根树为例，解释几种常见的求最近公共祖先（LCA）的算法，并给出对应的 Python 实现。你提到的 **DFS 序** 在实际讨论中常被用来指代 **倍增法**（Binary Lifting），因为它需要一次 DFS 预处理深度和父亲；而 **欧拉序** 指代的是将 LCA 转化为 RMQ 的经典在线算法。为保持术语清晰，下文将分别实现：

- **欧拉序 + ST 表**（在线，预处理 \(O(n\log n)\)，查询 \(O(1)\)）
- **倍增法**（在线，预处理 \(O(n\log n)\)，查询 \(O(\log n)\)）
- **Tarjan 离线算法**（离线，\(O(n+q)\)）
- **树链剖分**（在线，预处理 \(O(n)\)，查询 \(O(\log n)\)）

---

## 1. 欧拉序 + ST 表求 LCA

### 原理
- 对树做一次深度优先遍历，**每经过一个结点（包括回溯）就将其记录到欧拉序列中**，同时记录对应深度。
- 结点 \(u\) 第一次出现的位置记为 \(\text{first}[u]\)。
- 对于询问 \(\text{LCA}(u,v)\)，只需在欧拉序列的区间 \([\text{first}[u], \text{first}[v]]\) 中找出深度最小的结点，该结点即为 LCA。
- 区间最小值查询通过 **ST 表** 实现 \(O(1)\) 查询。

**空间复杂度**：欧拉序列长度 \(2n-1\)，ST 表大小 \(O(n\log n)\)。  
**优缺点**：查询极快，但空间常数较大（需开两倍结点数的数组）。

```python
import sys
sys.setrecursionlimit(1 << 25)

class EulerTourLCA:
    def __init__(self, n, edges, root=0):
        """
        n: 结点数 (编号 0 ~ n-1)
        edges: 邻接表，如 [[1,2],[0],...]
        root: 根结点编号
        """
        self.n = n
        self.euler = []          # 欧拉序列中的结点
        self.depth_seq = []      # 对应深度
        self.first = [-1] * n    # 每个结点在欧拉序列中首次出现的位置
        
        # DFS 生成欧拉序列
        stack = [(root, 0, 0)]   # (node, parent, depth)
        # 用迭代模拟递归，手动记录状态
        # 为了正确记录回溯，使用栈元素 (node, parent, depth, state)
        # state=0: 第一次访问; state=1: 离开该结点
        stack = [(root, -1, 0, 0)]
        while stack:
            u, p, d, state = stack.pop()
            if state == 0:
                # 第一次进入 u
                self.first[u] = len(self.euler)
                self.euler.append(u)
                self.depth_seq.append(d)
                # 先压入离开标记，再压入子结点
                stack.append((u, p, d, 1))
                for v in edges[u][::-1]:  # 逆序保证子结点按原序处理
                    if v != p:
                        stack.append((v, u, d+1, 0))
            else:
                # 离开 u，记录回溯（根结点可以不记录，但为统一长度也记录）
                if p != -1:
                    self.euler.append(p)
                    self.depth_seq.append(d-1)
        
        # 构建 ST 表 (记录深度最小值的下标)
        m = len(self.depth_seq)
        log_m = m.bit_length()
        self.st = [list(range(m)) for _ in range(log_m)]
        for i in range(m):
            self.st[0][i] = i
        
        for j in range(1, log_m):
            step = 1 << (j-1)
            for i in range(m - (1 << j) + 1):
                left = self.st[j-1][i]
                right = self.st[j-1][i+step]
                self.st[j][i] = left if self.depth_seq[left] < self.depth_seq[right] else right
        
    def query(self, u, v):
        """返回 u 和 v 的最近公共祖先"""
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l, r = r, l
        length = r - l + 1
        k = length.bit_length() - 1
        left_idx = self.st[k][l]
        right_idx = self.st[k][r - (1 << k) + 1]
        if self.depth_seq[left_idx] < self.depth_seq[right_idx]:
            return self.euler[left_idx]
        else:
            return self.euler[right_idx]
```

---

## 2. 倍增法 (Binary Lifting)

### 原理
- 用一次 DFS 预处理每个结点的 **深度** 和 **\(2^k\) 级祖先**。
- 查询时先将两个结点提到同一深度，然后一起向上跳。

**空间复杂度**：`up` 表大小 \(O(n\log n)\)，**比欧拉序更省空间**（约 \(n\log n\) 对 \(2n\) 基础数组 + ST 表）。  
**优缺点**：实现简单，预处理与查询均为对数复杂度，在大多数场景下足够优秀，即你提到的 **“DFS 序”** 的常用指代。

```python
class BinaryLiftingLCA:
    def __init__(self, n, edges, root=0):
        self.n = n
        self.LOG = (n).bit_length()
        self.up = [[-1] * n for _ in range(self.LOG)]
        self.depth = [0] * n
        
        # 迭代 DFS 建树
        stack = [(root, -1, 0)]
        while stack:
            u, p, d = stack.pop()
            self.depth[u] = d
            self.up[0][u] = p
            for v in edges[u]:
                if v != p:
                    stack.append((v, u, d+1))
        
        # 倍增预处理
        for k in range(1, self.LOG):
            for v in range(n):
                if self.up[k-1][v] != -1:
                    self.up[k][v] = self.up[k-1][self.up[k-1][v]]
    
    def query(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # 提升 u 到与 v 同深度
        diff = self.depth[u] - self.depth[v]
        for k in range(self.LOG):
            if diff & (1 << k):
                u = self.up[k][u]
        if u == v:
            return u
        # 一起向上跳
        for k in range(self.LOG-1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u = self.up[k][u]
                v = self.up[k][v]
        return self.up[0][u]
```

---
## 3. Tarjan 离线算法

### 原理
- 使用并查集，在 DFS 过程中处理所有询问。
- 当离开一个结点时，将其与父结点合并，并标记该结点已访问。
- 处理与当前结点相关的询问：若另一结点已被访问，则它的祖先（并查集的根）即为 LCA。

**复杂度**：\(O(n + q)\)，其中 \(q\) 为询问数。  
**优缺点**：处理批量询问极快，但必须一次性读入所有询问，且代码实现略复杂于倍增。

```python
class TarjanLCA:
    def __init__(self, n, edges, queries, root=0):
        """
        queries: 列表，每个元素为 (u, v, idx) 表示询问 u,v，答案填入 ans[idx]
        """
        self.n = n
        self.edges = edges
        self.queries = [[] for _ in range(n)]
        for u, v, idx in queries:
            self.queries[u].append((v, idx))
            self.queries[v].append((u, idx))
        
        self.parent = list(range(n))
        self.ancestor = list(range(n))
        self.visited = [False] * n
        self.ans = [0] * len(queries)
        
        self._dfs(root, -1)
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def _dfs(self, u, p):
        self.ancestor[u] = u
        for v in self.edges[u]:
            if v != p:
                self._dfs(v, u)
                # 合并
                self.parent[v] = u
                self.ancestor[self.find(u)] = u
        self.visited[u] = True
        for v, idx in self.queries[u]:
            if self.visited[v]:
                self.ans[idx] = self.ancestor[self.find(v)]
```

---

## 4. 树链剖分 (Heavy-Light Decomposition)

### 原理
- 第一遍 DFS 计算子树大小、深度、父亲和重儿子。
- 第二遍 DFS 分配链顶 `top`，并赋予 DFS 序（用于线段树等，求 LCA 时可不用）。
- 查询 LCA 时，不断将链顶深度较大的结点向上跳，直到两结点在同一链上。

**复杂度**：预处理 \(O(n)\)，查询 \(O(\log n)\)，**常数极小**。  
**优缺点**：非常适合需要同时维护路径信息的问题；若仅求 LCA，代码稍长，但运行效率高。

```python
class HLD_LCA:
    def __init__(self, n, edges, root=0):
        self.n = n
        self.edges = edges
        self.parent = [-1] * n
        self.depth = [0] * n
        self.size = [0] * n
        self.heavy = [-1] * n
        self.head = [0] * n   # 链顶
        
        # 第一遍 DFS：求 size, heavy
        stack = [(root, -1, 0)]  # (node, parent, depth)
        order = []
        while stack:
            u, p, d = stack.pop()
            self.parent[u] = p
            self.depth[u] = d
            order.append(u)
            for v in edges[u]:
                if v != p:
                    stack.append((v, u, d+1))
        
        for u in reversed(order):
            self.size[u] = 1
            max_sub = 0
            for v in edges[u]:
                if v != self.parent[u]:
                    self.size[u] += self.size[v]
                    if self.size[v] > max_sub:
                        max_sub = self.size[v]
                        self.heavy[u] = v
        
        # 第二遍 DFS：分配 head
        stack = [(root, root)]
        while stack:
            u, h = stack.pop()
            self.head[u] = h
            # 先处理重儿子
            if self.heavy[u] != -1:
                stack.append((self.heavy[u], h))
            for v in edges[u]:
                if v != self.parent[u] and v != self.heavy[u]:
                    stack.append((v, v))
    
    def query(self, u, v):
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            u = self.parent[self.head[u]]
        return u if self.depth[u] < self.depth[v] else v
```

---

## 算法对比总结

| 方法            | 预处理时间     | 单次查询时间  | 空间复杂度     | 在线/离线 | 代码难度 |
| --------------- | -------------- | ------------- | -------------- | --------- | -------- |
| 欧拉序 + ST 表  | \(O(n\log n)\) | \(O(1)\)      | \(O(n\log n)\) | 在线      | 中等     |
| 倍增法 (DFS 序) | \(O(n\log n)\) | \(O(\log n)\) | \(O(n\log n)\) | 在线      | 简单     |
| Tarjan 离线     | \(O(n+q)\)     | \(O(1)\) 均摊 | \(O(n+q)\)     | 离线      | 中等     |
| 树链剖分        | \(O(n)\)       | \(O(\log n)\) | \(O(n)\)       | 在线      | 中等     |

你提到的 **DFS 序** 在常规语境下与倍增法高度重合：都需要一次 DFS 预处理深度和父亲，然后利用二进制跳跃求解。其优势在于 **代码直观、空间适中**，且相比欧拉序无需担心两倍数组。而 **欧拉序 + ST 表** 提供了理论最优的 \(O(1)\) 查询，但 ST 表建表代价及空间占用是其短板。

当需要处理大量在线查询且对单次查询延迟有极致要求时，欧拉序 + ST 表更合适；  
若追求简洁、稳健，或需要同时维护路径信息，树链剖分是工程上的优秀选择；  
若所有询问已知且希望总体复杂度最优，则 Tarjan 离线算法是最佳选项。