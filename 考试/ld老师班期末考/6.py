s=input()
ans=0
current=0
for i in s:
    if i=='E':
        current+=1
    else:
        current-=1
    if current>ans:
        ans=current
print(ans)
    