from collections import defaultdict
m,n,k=map(int,input().split())
dic=defaultdict(list)
li=[]
for i in range(m,n):
    sum=0
    a=i
    while i!=0:
        sum+=i%10
        i//=10
    if sum%k==0:
        dic[sum//k].append(a)
for i in dic:
    li.append(i)
li.sort()
for i in li:
    print(','.join(map(str,dic[i])))



