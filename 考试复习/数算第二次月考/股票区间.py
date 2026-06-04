n=int(input())
stack1=[]
stack2=[]
stack1.append((float('inf'),-1))
stack2.append((-float('inf'),-1))
ans=0
for i in range(n):
    t=int(input())
    while stack1 and stack1[-1][0]<t:
        stack1.pop()
    while stack2 and stack2[-1][0]>t:
        stack2.pop()
    stack1.append((t,i))
    stack2.append((t,i))
    if stack1[-2][1]<stack2[-2][1]:
        j=-2
        while j>-len(stack2) and stack1[-2][1]<stack2[j-1][1] and stack2[j][0]!=stack2[j-1][0] :
            j-=1
        ans=max(ans,i-stack2[j][1]+1)    
print(ans)
    
