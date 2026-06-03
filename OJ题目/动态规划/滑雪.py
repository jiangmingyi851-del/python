import sys
def longest(mar,r,c):
    l1=[]
    for _ in range(r):
        for j in range(c):
            l1.append((_,j,mar[_][j]))
    l2=sorted(l1, key=lambda x:x[2])
    dire=[(0,1),(0,-1),(1,0),(-1,0)]
    length=[[1]*c for _ in range(r)]
    ans=1
    for i,j,height in l2:
        for dx,dy in dire:
            x,y=i+dx,j+dy
            if 0<=x<r and 0<=y<c:
                if mar[x][y]<height:
                    length[i][j]=max(length[i][j],length[x][y]+1)
                    ans=max(ans,length[i][j])
    return ans
r,c=map(int,sys.stdin.readline().split())
l0=[]
for _ in range(r):
    l=list(map(int,sys.stdin.readline().split()))
    l0.append(l)
print(longest(l0,r,c))

