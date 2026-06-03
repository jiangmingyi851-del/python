from collections import defaultdict
s,n=input().split()
k=int(n)
sum=[0]
dic={'a':0,'e':0,'i':0,'o':0,'u':0}
dic1=defaultdict(list)
dic1[0].append(-1)
num=0
for j,i in enumerate(s):
        if i in dic:
            sum.append(sum[-1]+1)
            for l in dic1[sum[-1]]:
                if ((j-l)//2)**2%k==0:
                    num+=1
            dic1[sum[-1]].append(j)
        else:
            sum.append(sum[-1]-1)
            for l in dic1[sum[-1]]:
                if ((j-l)//2)**2%k==0:
                    num+=1
            dic1[sum[-1]].append(j)
print(num)


