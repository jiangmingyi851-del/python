from collections import defaultdict
import bisect
n,d=map(int,input().split())
a=list(map(int,input().split()))
INF = 10**9+1
class SegmentTree:
    def __init__(self, n, data):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.min_tree = [INF] * (2 * self.size)
        self.max_tree = [0] * (2 * self.size)
        for i in range(n):
            self.min_tree[self.size + i] = data[i]
            self.max_tree[self.size + i] = data[i]
        for i in range(n, self.size):
            self.min_tree[self.size + i] = INF
            self.max_tree[self.size + i] = 0
        for i in range(self.size-1, 0, -1):
            self.min_tree[i] = min(self.min_tree[2*i], self.min_tree[2*i+1])
            self.max_tree[i] = max(self.max_tree[2*i], self.max_tree[2*i+1])

    def update(self, index, value):
        i = self.size + index  # 计算在线段树数组中的位置
        if value==None:
            self.min_tree[i] = INF  # 将该位置的最小值标记为无穷大（表示已删除）
            self.max_tree[i] = 0  # 将该位置的最大值标记为负无穷大（表示已删除）
        else:
            self.min_tree[i] = value  # 更新该位置的最小值
            self.max_tree[i] = value  # 更新该位置的最大值
            i //= 2  # 移动到父节点
        while i:  # 循环更新所有祖先节点，直到根节点
            self.min_tree[i] = min(self.min_tree[2*i], self.min_tree[2*i+1])  # 更新父节点的最小值
            self.max_tree[i] = max(self.max_tree[2*i], self.max_tree[2*i+1])  # 更新父节点的最大值
            i //= 2  # 继续向上移动到更高级的父节点

    def query(self, l, r):
        l += self.size  # 将原始索引转换为线段树中的叶子节点索引
        r += self.size  # 将原始索引转换为线段树中的叶子节点索引
        res_min = INF   # 初始化最小值为无穷大
        res_max = 0  # 初始化最大值为负无穷大
        while l < r:    # 当查询区间不为空时循环
            if l & 1:   # 如果 l 是右子节点（奇数索引）
                res_min = min(res_min, self.min_tree[l])  # 更新最小值
                res_max = max(res_max, self.max_tree[l])  # 更新最大值
                l += 1  # 将 l 向右移动一位
            if r & 1:   # 如果 r 是右子节点（奇数索引）
                r -= 1  # 先将 r 向左移动一位
                res_min = min(res_min, self.min_tree[r])  # 更新最小值
                res_max = max(res_max, self.max_tree[r])  # 更新最大值
            l //= 2     # 将 l 移动到父节点层
            r //= 2     # 将 r 移动到父节点层
        return (res_min, res_max)  # 返回查询结果
vals=sorted(set(a))
val_to_idx = {v: i for i, v in enumerate(vals)}
m=len(vals)
layer=[0]*m
layer[val_to_idx[a[0]]]=1
st=SegmentTree(m,layer)
cur_queue=[[a[0]]]
for i in range(1,n):
    left=bisect.bisect_left(vals,a[i]-d)
    right=bisect.bisect_right(vals,a[i]+d)
    l1,r1=st.query(0,left) if left>0 else (INF,0)
    l2,r2=st.query(right,m) if right<m else (INF,0)
    layer[val_to_idx[a[i]]]=max(r1,r2)+1
    if layer[val_to_idx[a[i]]]>len(cur_queue):
        cur_queue.append([a[i]])
    else:
        cur_queue[layer[val_to_idx[a[i]]]-1].append(a[i])
    st.update(val_to_idx[a[i]],layer[val_to_idx[a[i]]])
ans=[]
for j in cur_queue:
    j.sort()
    ans.extend(j)
print(' '.join(map(str,ans)))
