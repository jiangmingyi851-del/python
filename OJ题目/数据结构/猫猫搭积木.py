# n,q,s=map(int,input().split())
# parent=[i for i in range(n+1)]
# comp=[[i] for i in range(n+1)]
# def find(x):
#     if parent[x]!=x:
#         parent[x]=find(parent[x])
#     return parent[x]
# def union(x,y):
#     parent[find(x)]=find(y)
# ans=n
# for i in range(q):
#     a,b=map(int,input().split())
#     u=find(a)
#     v=find(b)
#     if u==v:
#         print(ans)
#     else:
#         if (len(comp[u])+len(comp[v]))>=s:
#             ans=ans+len(comp[u])+len(comp[v])-2
#             for i in comp[u]:
#                 parent[i]=i
#                 comp[i]=[i]
#             for i in comp[v]:
#                 parent[i]=i
#                 comp[i]=[i]
#             print(ans)
#         else:
#             union(u,v)
#             ans=ans-1
#             comp[v].extend(comp[u])
#             comp[u]=[]
#             print(ans)

class Node:
    def __init__(self,num):
        self.parent=self
        self.num=num
        self.sum=1
def main():
    n,q,s=map(int,input().split())
    li=[Node(i) for i in range(1,n+1)]
    def find(x):
        cur=x
        if x.parent!=x:
            x.parent,ind=find(x.parent)
        return (x.parent,x.parent.num)

    def union(a,b):
        if a!=b:
            a.parent=b
            a.sum+=b.sum
            b.sum=a.sum
        return (b,b.num)
    ans=n
    for i in range(q):
        a,b=map(int,input().split())
        roota,numa=find(li[a-1])
        if roota.num==0:
            roota=Node(a)
            li[a-1]=roota
        rootb,numb=find(li[b-1])
        if rootb.num==0:
            rootb=Node(b)
            li[b-1]=rootb
        if roota==rootb:
            print(ans)
            continue
        union(roota,rootb)
        if rootb.sum>=s:
            r=rootb.sum
            rootb.sum=0
            li[numb-1]=Node(numb)
            ans=ans+r-2
            print(ans)
        else:
            ans-=1
            print(ans)

        
if __name__=='__main__':
    main()           
