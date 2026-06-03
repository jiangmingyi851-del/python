import sys
data=sys.stdin.read().strip().split()
n,m=map(int,data[:2])
s=int(data[2])
v=float(data[3])
edges=[]
idx=4
for i in range(m):
    a=int(data[idx])
    b=int(data[idx+1])
    a_to_b=float(data[idx+2])
    c_ab=float(data[idx+3])
    b_to_a=float(data[idx+4])
    c_ba=float(data[idx+5])
    edges.append((a,b,a_to_b,c_ab))
    edges.append((b,a,b_to_a,c_ba))
    idx+=6
dist=[0.0]*(n+1)
dist[s]=v
for _ in range(n-1):
    for a,b,a_to_b,c_ab in edges:
        updated=False
        if (dist[a]-c_ab)*a_to_b>dist[b]:
            dist[b]=(dist[a]-c_ab)*a_to_b
            updated=True
        if dist[s]>v:
            print('YES')
            exit()
    if not updated:
        print('NO')
        exit()
for a,b,a_to_b,c_ab in edges:
        if (dist[a]-c_ab)*a_to_b>dist[b]:
            print('YES')
            exit()
print('NO')