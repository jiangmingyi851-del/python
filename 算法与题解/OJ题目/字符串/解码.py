n=int(input().strip())
a=input().strip()
li=[]
hi=[]
str=""
head=0
for i,j in enumerate(a):
    if head%2==0:
        hi.append(j)
        if i%n==n-1:
            li.append(hi)
            hi=[]
            head+=1
    else:
        hi.insert(0,j)
        if i%n==n-1:
            li.append(hi)
            hi=[]
            head+=1
for i in range(n):
    for j in range(len(li)):
        str+=li[j][i]
print(str)
