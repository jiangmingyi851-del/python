n=int(input())
stack=[]
final=[]
ans=0
for i in range(n):
    s=input()
    if s=='remove':
        if stack[-1]!=len(final)+1:
            ans+=1
            stack.sort(reverse=True)
        a=stack.pop()
        final.append(a)
    else:
        a,b=input.split()
        b=int(b)
        stack.append(b)
print(ans)