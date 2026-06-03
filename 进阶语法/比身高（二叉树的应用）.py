class human:
    def __init__(self,height):
        self.height=height
        self.used=False


import sys
N,D=map(int,sys.stdin.readline().strip().split())
H=[human(map(int,sys.stdin.readline().strip())) for _ in range(N)]
sh=sorted(H,key=lambda x:x.height)
def dic_list(lis,d,slis):
     ans=[]
     if len(slis)==0:
         return ans
     for si in slis:
         if si.used==True:
             continue
         si.used=True
         if lis.index(si)==0:
             return dic_list(lis,d,slis[1:]).append(si.height)
         for j in [i for i in lis[:lis.index(si)] if i.used==False ]:
             if  abs(si.height-j.height)<=d:
                continue
             else:
                si.used=False
                break
             ans.append(si.height)
             ans.extend(dic_list(lis,d,slis))
     return ans


import heapq
import sys

INF = 10**18

class SegmentTree:
    def __init__(self, n, data):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.min_tree = [INF] * (2 * self.size)
        self.max_tree = [-INF] * (2 * self.size)
        for i in range(n):
            self.min_tree[self.size + i] = data[i]
            self.max_tree[self.size + i] = data[i]
        for i in range(n, self.size):
            self.min_tree[self.size + i] = INF
            self.max_tree[self.size + i] = -INF
        for i in range(self.size-1, 0, -1):
            self.min_tree[i] = min(self.min_tree[2*i], self.min_tree[2*i+1])
            self.max_tree[i] = max(self.max_tree[2*i], self.max_tree[2*i+1])
    
    def update(self, index, value):
        i = self.size + index
        self.min_tree[i] = INF
        self.max_tree[i] = -INF
        i //= 2
        while i:
            self.min_tree[i] = min(self.min_tree[2*i], self.min_tree[2*i+1])
            self.max_tree[i] = max(self.max_tree[2*i], self.max_tree[2*i+1])
            i //= 2

    def query(self, l, r):
        l += self.size
        r += self.size
        res_min = INF
        res_max = -INF
        while l < r:
            if l & 1:
                res_min = min(res_min, self.min_tree[l])
                res_max = max(res_max, self.max_tree[l])
                l += 1
            if r & 1:
                r -= 1
                res_min = min(res_min, self.min_tree[r])
                res_max = max(res_max, self.max_tree[r])
            l //= 2
            r //= 2
        return (res_min, res_max)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0]); D = int(data[1])
    H = []
    for i in range(n):
        H.append(int(data[2+i]))
    
    seg_tree = SegmentTree(n, H)
    heap = []
    for i in range(n):
        heapq.heappush(heap, (H[i], i))
    
    ans = []
    S = set()
    
    for _ in range(n):
        while True:
            if not heap:
                break
            height, pos = heapq.heappop(heap)
            min_val, max_val = seg_tree.query(pos, pos+1)
            if min_val == INF and max_val == -INF:
                continue
            if pos == 0:
                break
            left_min, left_max = seg_tree.query(0, pos)
            if left_min >= height - D and left_max <= height + D:
                break
            S.add((height, pos))
        ans.append(height)
        seg_tree.update(pos, None)
        while S:
            item = S.pop()
            heapq.heappush(heap, item)
            
    for a in ans:
        print(a)

if __name__ == '__main__':
    main()
             

                
    

