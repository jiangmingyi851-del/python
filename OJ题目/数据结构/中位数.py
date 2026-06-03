from collections import deque,defaultdict
import heapq
class MedianFinder:
    def __init__(self):
        self.left=[]
        self.right=[]
        self.list=deque()
        self.median=0
        self.balance=0
        self.dele=defaultdict(int)
    
    def addNum(self,num):
        self.list.append(num)
        if self.left or num<=self.left[0]:
            heapq.heappush(self.left,-num)
            self.balance+=1
        else:
            heapq.heappush(self.right,num)
            self.balance-=1
        self._rebalance()
    def _rebalance(self):
        if abs(self.balance)>1:
            if self.balance>1:
                self._clean()
                heapq.heappush(self.right,-heapq.heappop(self.left))
                self.balance-=2
            else:
                self._clean()
                heapq.heappush(self.left,-heapq.heappop(self.right))
                self.balance+=2
            self._clean()
    def _clean(self):
        while self.left and self.dele.get(self.left[0],0)>0:
            val=-heapq.heappop(self.left)
            self.dele[val]-=1
            if self.dele[val]==0:
                del self.dele[val]
        while self.right and self.dele.get(self.right[0],0)>0:
            val=heapq.heappop(self.right)
            self.dele[val]-=1
            if self.dele[val]==0:
                del self.dele[val]
    def delete(self):
        if not self.list:
            return
        val=self.list.popleft()
        self.dele[val]+=1
        if val<=self.left[0]:
            self.balance-=1
        else:
            self.balance+=1
        self._rebalance()
    def query(self):
        if not self.list:
            return None
        if self.balance>0:
            return -self.left[0]
        elif self.balance<0:
            return self.right[0]
        else:
            return (-self.left[0]+self.right[0])/2
            
            
        



n=int(input())
m=MedianFinder()
for i in range(n):
    a=input().strip()
    if a=='del':
        m.delete()
    elif a=='query':
        b=m.query()
        if int(b)==b:
            print(int(b))
        else:
            print(b)
    else:
        b,c=a.split()
        m.addNum(int(c))

        
 






            
    


        
