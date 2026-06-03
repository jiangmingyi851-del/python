l,m=map(int,input().split())
li=[]
for i in range(m):
    a,b=map(int,input().split())
    li.append((a,b))
li.sort()
ans=[]
ans.append(li[0])
for i in range(1,m):
    if li[i][0]<=ans[-1][1]:
        ans[-1]=(ans[-1][0],max(ans[-1][1],li[i][1]))
    else:
        ans.append(li[i])
an=l+1
for i in ans:
    an-=i[1]-i[0]+1
print(an)
    

    